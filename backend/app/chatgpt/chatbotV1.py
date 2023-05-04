#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:chatbotV1.py
# author:song
# datetime:2023/4/20 17:34
# software: PyCharm

"""
this is function  description 
"""
from __future__ import annotations

import base64
import contextlib
import json
import time
import uuid
from os import getenv
from pathlib import Path
from typing import Generator

import requests
from OpenAIAuth import Authenticator
from OpenAIAuth import Error as AuthError
from httpx import AsyncClient

from config.globals import config
from . import typings as t
from .utils import logger, log

if config.get("chatgpt_base_url"):
    BASE_URL = config.get("chatgpt_base_url")
else:
    BASE_URL = config.get("chatgpt_proxy_url")


class Chatbot:
    """
    Chatbot class for ChatGPT
    """

    @logger(is_timed=True)
    def __init__(
            self,
            config: dict[str, str],
            conversation_id: str | None = None,
            parent_id: str | None = None,
            session_client=None,
            lazy_loading: bool = True,
            base_url: str | None = None,
    ) -> None:
        """Initialize a chatbot

        Args:
            config (dict[str, str]): Login and proxy info. Example:
                {
                    "email": "OpenAI account email",
                    "password": "OpenAI account password",
                    "session_token": "<session_token>"
                    "access_token": "<access_token>"
                    "proxy": "<proxy_url_string>",
                    "paid": True/False, # whether this is a plus account
                    "_puid": "puid", # V4 only, if it is set, base_url will be changed to https://chat.openai.com/backend-api/
                }
                More details on these are available at https://github.com/acheong08/ChatGPT#configuration
            conversation_id (str | None, optional): Id of the conversation to continue on. Defaults to None.
            parent_id (str | None, optional): Id of the previous response message to continue on. Defaults to None.
            session_client (_type_, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_
        """
        user_home = getenv("HOME")
        if user_home is None:
            user_home = Path().cwd()
            self.cache_path = Path(Path().cwd(), ".chatgpt_cache.json")
        else:
            # mkdir ~/.config/revChatGPT
            if not Path(user_home, ".config").exists():
                Path(user_home, ".config").mkdir()
            if not Path(user_home, ".config", "revChatGPT").exists():
                Path(user_home, ".config", "revChatGPT").mkdir()
            self.cache_path = Path(user_home, ".config",
                                   "revChatGPT", "cache.json")

        self.config = config
        self.session = session_client() if session_client else requests.Session()
        if "email" in config and "password" in config:
            try:
                cached_access_token = self.__get_cached_access_token(
                    self.config.get("email", None),
                )
            except t.Error as error:
                if error.code == 5:
                    raise
                cached_access_token = None
            if cached_access_token is not None:
                self.config["access_token"] = cached_access_token

        if "proxy" in config:
            if not isinstance(config["proxy"], str):
                error = TypeError("Proxy must be a string!")
                raise error
            proxies = {
                "http": config["proxy"],
                "https": config["proxy"],
            }
            if isinstance(self.session, AsyncClient):
                proxies = {
                    "http://": config["proxy"],
                    "https://": config["proxy"],
                }
                self.session = AsyncClient(proxies=proxies)
            else:
                self.session.proxies.update(proxies)
        self.conversation_id = conversation_id
        self.parent_id = parent_id
        self.conversation_mapping = {}
        self.conversation_id_prev_queue = []
        self.parent_id_prev_queue = []
        self.lazy_loading = lazy_loading

        if "_puid" in self.config and self.config["_puid"]:
            self.base_url = "https://chat.openai.com/backend-api/"
            self.__set_puid(self.config["_puid"])
        else:
            self.base_url = base_url or BASE_URL

        self.__check_credentials()

    @logger(is_timed=True)
    def __check_credentials(self) -> None:
        """Check login info and perform login

        Any one of the following is sufficient for login. Multiple login info can be provided at the same time and they will be used in the order listed below.
            - access_token
            - session_token
            - email + password

        Raises:
            Exception: _description_
            AuthError: _description_
        """
        if "access_token" in self.config:
            self.set_access_token(self.config["access_token"])
        elif "session_token" in self.config:
            pass
        elif "email" not in self.config or "password" not in self.config:
            error = t.AuthenticationError(
                "Insufficient login details provided!")
            raise error
        if "access_token" not in self.config:
            try:
                self.login()
            except AuthError as error:
                print(error.details)
                print(error.status_code)
                raise error

    @logger(is_timed=False)
    def __set_puid(self, puid: str) -> None:
        self.session.cookies.update(
            {
                "_puid": puid,
            },
        )

    @logger(is_timed=False)
    def set_access_token(self, access_token: str) -> None:
        """Set access token in request header and self.config, then cache it to file.

        Args:
            access_token (str): access_token
        """
        self.session.headers.clear()
        self.session.headers.update(
            {
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Openai-Assistant-App-Id": "",
                "Connection": "close",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://chat.openai.com/chat",
            },
        )
        self.session.cookies.update(
            {
                "library": "revChatGPT",
            },
        )

        self.config["access_token"] = access_token

        email = self.config.get("email", None)
        if email is not None:
            self.__cache_access_token(email, access_token)

    @logger(is_timed=False)
    def __get_cached_access_token(self, email: str | None) -> str | None:
        """Read access token from cache

        Args:
            email (str | None): email of the account to get access token

        Raises:
            Error: _description_
            Error: _description_
            Error: _description_

        Returns:
            str | None: access token string or None if not found
        """
        email = email or "default"
        cache = self.__read_cache()
        access_token = cache.get("access_tokens", {}).get(email, None)

        # Parse access_token as JWT
        if access_token is not None:
            try:
                # Split access_token into 3 parts
                s_access_token = access_token.split(".")
                # Add padding to the middle part
                s_access_token[1] += "=" * \
                                     ((4 - len(s_access_token[1]) % 4) % 4)
                d_access_token = base64.b64decode(s_access_token[1])
                d_access_token = json.loads(d_access_token)
            except base64.binascii.Error:
                error = t.Error(
                    source="__get_cached_access_token",
                    message="Invalid access token",
                    code=t.ErrorType.INVALID_ACCESS_TOKEN_ERROR,
                )
                raise error from None
            except json.JSONDecodeError:
                error = t.Error(
                    source="__get_cached_access_token",
                    message="Invalid access token",
                    code=t.ErrorType.INVALID_ACCESS_TOKEN_ERROR,
                )
                raise error from None

            exp = d_access_token.get("exp", None)
            if exp is not None and exp < time.time():
                error = t.Error(
                    source="__get_cached_access_token",
                    message="Access token expired",
                    code=t.ErrorType.EXPIRED_ACCESS_TOKEN_ERROR,
                )
                raise error

        return access_token

    @logger(is_timed=False)
    def __cache_access_token(self, email: str, access_token: str) -> None:
        """Write an access token to cache

        Args:
            email (str): account email
            access_token (str): account access token
        """
        email = email or "default"
        cache = self.__read_cache()
        if "access_tokens" not in cache:
            cache["access_tokens"] = {}
        cache["access_tokens"][email] = access_token
        self.__write_cache(cache)

    @logger(is_timed=False)
    def __write_cache(self, info: dict) -> None:
        """Write cache info to file

        Args:
            info (dict): cache info, current format
            {
                "access_tokens":{"someone@example.com": 'this account's access token', }
            }
        """
        dirname = self.cache_path.home() or Path(".")
        dirname.mkdir(parents=True, exist_ok=True)
        json.dump(info, open(self.cache_path, "w", encoding="utf-8"), indent=4)

    @logger(is_timed=False)
    def __read_cache(self):
        try:
            cached = json.load(open(self.cache_path, encoding="utf-8"))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            cached = {}
        return cached

    @logger(is_timed=True)
    def login(self) -> None:
        if (
                "email" not in self.config or "password" not in self.config
        ) and "session_token" not in self.config:
            log.error("Insufficient login details provided!")
            error = t.AuthenticationError(
                "Insufficient login details provided!")
            raise error
        auth = Authenticator(
            email_address=self.config.get("email"),
            password=self.config.get("password"),
            proxy=self.config.get("proxy"),
        )
        if self.config.get("session_token"):
            log.debug("Using session token")
            auth.session.cookies.set(
                "__Secure-next-auth.session-token",
                self.config["session_token"],
            )
            auth.get_access_token()
            if auth.access_token is None:
                del self.config["session_token"]
                self.login()
                return
        else:
            log.debug("Using authenticator to get access token")
            auth.begin()
            auth.get_access_token()

        self.set_access_token(auth.access_token)

    @logger(is_timed=True)
    def __send_request(
            self,
            data: dict,
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> Generator[dict, None, None]:
        log.debug("Sending the payload")

        cid, pid = data["conversation_id"], data["parent_message_id"]
        model, message = None, ""

        self.conversation_id_prev_queue.append(cid)
        self.parent_id_prev_queue.append(pid)
        response = self.session.post(
            url=f"{self.base_url}conversation",
            data=json.dumps(data),
            timeout=timeout,
            stream=True,
        )
        self.__check_response(response)

        finish_details = None
        for line in response.iter_lines():
            # remove b' and ' at the beginning and end and ignore case
            line = str(line)[2:-1]
            if line.lower() == "internal server error":
                log.error(f"Internal Server Error: {line}")
                error = t.Error(
                    source="ask",
                    message="Internal Server Error",
                    code=t.ErrorType.SERVER_ERROR,
                )
                raise error
            if not line or line is None:
                continue
            if "data: " in line:
                line = line[6:]
            if line == "[DONE]":
                break

            line = line.replace('\\"', '"')
            line = line.replace("\\'", "'")
            line = line.replace("\\\\", "\\")

            try:
                line = json.loads(line)
            except json.decoder.JSONDecodeError:
                continue
            if not self.__check_fields(line):
                raise ValueError(f"Field missing. Details: {str(line)}")
            if line.get("message").get("author").get("role") != "assistant":
                continue
            message: str = line["message"]["content"]["parts"][0]
            cid = line["conversation_id"]
            pid = line["message"]["id"]
            metadata = line["message"].get("metadata", {})
            model = metadata.get("model_slug", None)
            finish_details = metadata.get(
                "finish_details", {"type": None})["type"]
            yield {
                "message": message,
                "conversation_id": cid,
                "parent_id": pid,
                "model": model,
                "finish_details": finish_details,
                "end_turn": line["message"].get("end_turn", True),
                "recipient": line["message"].get("recipient", "all"),
            }

        self.conversation_mapping[cid] = pid
        if pid is not None:
            self.parent_id = pid
        if cid is not None:
            self.conversation_id = cid

        if not (auto_continue and finish_details == "max_tokens"):
            return
        message = message.strip("\n")
        for i in self.continue_write(
                conversation_id=cid,
                model=model,
                timeout=timeout,
        ):
            i["message"] = message + i["message"]
            yield i

    @logger(is_timed=True)
    def post_messages(
            self,
            messages: list[dict],
            conversation_id: str | None = None,
            parent_id: str | None = None,
            model: str | None = None,
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> Generator[dict, None, None]:
        """Ask a question to the chatbot
        Args:
            messages (list[dict]): The messages to send
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str | None, optional): UUID for the message to continue on. Defaults to None.
            model (str | None, optional): The model to use. Defaults to None.
            auto_continue (bool, optional): Whether to continue the conversation automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.

        Yields: Generator[dict, None, None] - The response from the chatbot
            dict: {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str, # "max_tokens" or "stop"
                "end_turn": bool,
                "recipient": str,
            }
        """
        if parent_id and not conversation_id:
            raise t.Error(
                source="User",
                message="conversation_id must be set once parent_id is set",
                code=t.ErrorType.USER_ERROR,
            )

        if conversation_id and conversation_id != self.conversation_id:
            self.parent_id = None
        conversation_id = conversation_id or self.conversation_id
        parent_id = parent_id or self.parent_id or ""
        if not conversation_id and not parent_id:
            parent_id = str(uuid.uuid4())

        if conversation_id and not parent_id:
            if conversation_id not in self.conversation_mapping:
                if self.lazy_loading:
                    log.debug(
                        f"Conversation ID {conversation_id} not found in conversation mapping, try to get conversation history for the given ID",
                    )
                    with contextlib.suppress(Exception):
                        history = self.get_msg_history(conversation_id)
                        self.conversation_mapping[conversation_id] = history[
                            "current_node"
                        ]
                else:
                    self.__map_conversations()
            if conversation_id in self.conversation_mapping:
                parent_id = self.conversation_mapping[conversation_id]
            else:  # invalid conversation_id provided, treat as a new conversation
                conversation_id = None
                parent_id = str(uuid.uuid4())

        data = {
            "action": "next",
            "messages": messages,
            "conversation_id": conversation_id,
            "parent_message_id": parent_id,
            "model": model
                     or self.config.get("model")
                     or (
                         "text-davinci-002-render-paid"
                         if self.config.get("paid")
                         else "text-davinci-002-render-sha"
                     ),
        }

        yield from self.__send_request(
            data,
            timeout=timeout,
            auto_continue=auto_continue,
        )

    @logger(is_timed=True)
    def ask(
            self,
            prompt: str,
            conversation_id: str | None = None,
            parent_id: str | None = None,
            model: str | None = None,
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> Generator[dict, None, None]:
        """Ask a question to the chatbot
        Args:
            prompt (str): The question
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str | None, optional): UUID for the message to continue on. Defaults to None.
            model (str | None, optional): The model to use. Defaults to None.
            auto_continue (bool, optional): Whether to continue the conversation automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.

        Yields: Generator[dict, None, None] - The response from the chatbot
            dict: {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str, # "max_tokens" or "stop"
                "end_turn": bool,
                "recipient": str,
            }
        """
        messages = [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [prompt]},
            },
        ]

        yield from self.post_messages(
            messages,
            conversation_id=conversation_id,
            parent_id=parent_id,
            model=model,
            auto_continue=auto_continue,
            timeout=timeout,
        )

    @logger(is_timed=True)
    def continue_write(
            self,
            conversation_id: str | None = None,
            parent_id: str = "",
            model: str = "",
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> Generator[dict, None, None]:
        """let the chatbot continue to write
        Args:
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str | None, optional): UUID for the message to continue on. Defaults to None.
            model (str | None, optional): The model to use. Defaults to None.
            auto_continue (bool, optional): Whether to continue the conversation automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.

        Yields:
            dict: {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str, # "max_tokens" or "stop"
                "end_turn": bool,
                "recipient": str,
            }
        """
        if parent_id and not conversation_id:
            raise t.Error(
                source="User",
                message="conversation_id must be set once parent_id is set",
                code=t.ErrorType.USER_ERROR,
            )

        if conversation_id and conversation_id != self.conversation_id:
            self.parent_id = None
        conversation_id = conversation_id or self.conversation_id
        parent_id = parent_id or self.parent_id or ""
        if not conversation_id and not parent_id:
            parent_id = str(uuid.uuid4())

        if conversation_id and not parent_id:
            if conversation_id not in self.conversation_mapping:
                if self.lazy_loading:
                    log.debug(
                        f"Conversation ID {conversation_id} not found in conversation mapping, try to get conversation history for the given ID",
                    )
                    with contextlib.suppress(Exception):
                        history = self.get_msg_history(conversation_id)
                        self.conversation_mapping[conversation_id] = history[
                            "current_node"
                        ]
                else:
                    log.debug(
                        f"Conversation ID {conversation_id} not found in conversation mapping, mapping conversations",
                    )
                    self.__map_conversations()
            if conversation_id in self.conversation_mapping:
                parent_id = self.conversation_mapping[conversation_id]
            else:  # invalid conversation_id provided, treat as a new conversation
                conversation_id = None
                parent_id = str(uuid.uuid4())

        data = {
            "action": "continue",
            "conversation_id": conversation_id,
            "parent_message_id": parent_id,
            "model": model
                     or self.config.get("model")
                     or (
                         "text-davinci-002-render-paid"
                         if self.config.get("paid")
                         else "text-davinci-002-render-sha"
                     ),
        }

        yield from self.__send_request(
            data,
            timeout=timeout,
            auto_continue=auto_continue,
        )

    @logger(is_timed=False)
    def __check_fields(self, data: dict) -> bool:
        try:
            data["message"]["content"]
        except (TypeError, KeyError):
            return False
        return True

    @logger(is_timed=False)
    def __check_response(self, response: requests.Response) -> None:
        """Make sure response is success

        Args:
            response (_type_): _description_

        Raises:
            Error: _description_
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error = t.Error(
                source="OpenAI",
                message=response.text,
                code=response.status_code,
            )
            raise error from e

    @logger(is_timed=True)
    def get_conversations(
            self,
            offset: int = 0,
            limit: int = 20,
            encoding: str | None = None,
    ) -> list:
        """
        Get conversations
        :param offset: Integer
        :param limit: Integer
        """
        url = f"{self.base_url}conversations?offset={offset}&limit={limit}"
        response = self.session.get(url)
        self.__check_response(response)
        if encoding is not None:
            response.encoding = encoding
        data = json.loads(response.text)
        return data["items"]

    @logger(is_timed=True)
    def get_msg_history(self, convo_id: str, encoding: str | None = None) -> list:
        """
        Get message history
        :param id: UUID of conversation
        :param encoding: String
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = self.session.get(url)
        self.__check_response(response)
        if encoding is not None:
            response.encoding = encoding
        return json.loads(response.text)

    @logger(is_timed=True)
    def gen_title(self, convo_id: str, message_id: str) -> str:
        """
        Generate title for conversation
        """
        response = self.session.post(
            f"{self.base_url}conversation/gen_title/{convo_id}",
            data=json.dumps(
                {"message_id": message_id, "model": "text-davinci-002-render"},
            ),
        )
        self.__check_response(response)
        return response.json().get("title", "Error generating title")

    @logger(is_timed=True)
    def change_title(self, convo_id: str, title: str) -> None:
        """
        Change title of conversation
        :param id: UUID of conversation
        :param title: String
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = self.session.patch(url, data=json.dumps({"title": title}))
        self.__check_response(response)

    @logger(is_timed=True)
    def delete_conversation(self, convo_id: str) -> None:
        """
        Delete conversation
        :param id: UUID of conversation
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = self.session.patch(url, data='{"is_visible": false}')
        self.__check_response(response)

    @logger(is_timed=True)
    def clear_conversations(self) -> None:
        """
        Delete all conversations
        """
        url = f"{self.base_url}conversations"
        response = self.session.patch(url, data='{"is_visible": false}')
        self.__check_response(response)

    @logger(is_timed=False)
    def __map_conversations(self) -> None:
        conversations = self.get_conversations()
        histories = [self.get_msg_history(x["id"]) for x in conversations]
        for x, y in zip(conversations, histories):
            self.conversation_mapping[x["id"]] = y["current_node"]

    @logger(is_timed=False)
    def reset_chat(self) -> None:
        """
        Reset the conversation ID and parent ID.

        :return: None
        """
        self.conversation_id = None
        self.parent_id = str(uuid.uuid4())

    @logger(is_timed=False)
    def rollback_conversation(self, num: int = 1) -> None:
        """
        Rollback the conversation.
        :param num: Integer. The number of messages to rollback
        :return: None
        """
        for _ in range(num):
            self.conversation_id = self.conversation_id_prev_queue.pop()
            self.parent_id = self.parent_id_prev_queue.pop()
