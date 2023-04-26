#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:asyncChatbotV1.py
# author:song
# datetime:2023/4/20 17:36
# software: PyCharm

"""
this is function  description 
"""
from __future__ import annotations

import json
import uuid

import httpx
from httpx import AsyncClient
from config import Config
from typing import AsyncGenerator
from . import typings as t

from .chatbotV1 import Chatbot


class AsyncChatbot(Chatbot):
    """
    Async Chatbot class for ChatGPT
    """

    def __init__(
            self,
            config: dict,
            conversation_id: str | None = None,
            parent_id: str = "",
            base_url: str = "",
    ) -> None:
        """
        Same as Chatbot class, but with async methods.

        Note:
            AsyncChatbot is not compatible with OpenAI Web API, I don't know why the stream method doesn't work.
            (But the sync version works fine)
            So, if you want to use AsyncChatbot, you don't need to set the "_puid" parameter in the config.
        """
        super().__init__(
            config=config,
            conversation_id=conversation_id,
            parent_id=parent_id,
            session_client=AsyncClient,
            base_url=base_url,
        )

    async def __send_request(
            self,
            data: dict,
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> AsyncGenerator[dict, None]:
        cid, pid = data["conversation_id"], data["parent_message_id"]

        self.conversation_id_prev_queue.append(cid)
        self.parent_id_prev_queue.append(pid)
        message = ""

        finish_details = None
        response = None
        async with self.session.stream(
                method="POST",
                url=f"{self.base_url}conversation",
                data=json.dumps(data),
                timeout=timeout,
        ) as response:
            await self.__check_response(response)
            async for line in response.aiter_lines():
                if not line or line is None:
                    continue
                if "data: " in line:
                    line = line[6:]
                if "[DONE]" in line:
                    break

                try:
                    line = json.loads(line)
                except json.decoder.JSONDecodeError:
                    continue
                if not self.__check_fields(line):
                    raise ValueError(f"Field missing. Details: {str(line)}")

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
            if pid:
                self.parent_id = pid
            if cid:
                self.conversation_id = cid

        if not (auto_continue and finish_details == "max_tokens"):
            return
        async for msg in self.continue_write(
                conversation_id=cid,
                auto_continue=auto_continue,
                timeout=timeout,
        ):
            msg["message"] = message + msg["message"]
            yield msg

    async def post_messages(
            self,
            messages: list[dict],
            conversation_id: str | None = None,
            parent_id: str = "",
            model: str = "",
            auto_continue: bool = False,
            timeout: int = 360,
    ) -> AsyncGenerator[dict, None]:
        """Post messages to the chatbot

        Args:
            messages (list[dict]): the messages to post
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str, optional): UUID for the message to continue on. Defaults to "".
            model (str, optional): The model to use. Defaults to "".
            auto_continue (bool, optional): Whether to continue the conversation automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.

        Yields:
            AsyncGenerator[dict, None]: The response from the chatbot
            {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str,
                "end_turn": bool,
                "recipient": str,
            }
        """
        if parent_id and not conversation_id:
            error = t.Error(
                source="User",
                message="conversation_id must be set once parent_id is set",
                code=t.ErrorType.SERVER_ERROR,
            )
            raise error
        if conversation_id and conversation_id != self.conversation_id:
            self.parent_id = None
        conversation_id = conversation_id or self.conversation_id

        parent_id = parent_id or self.parent_id or ""
        if not conversation_id and not parent_id:
            parent_id = str(uuid.uuid4())
        if conversation_id and not parent_id:
            if conversation_id not in self.conversation_mapping:
                await self.__map_conversations()
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

        async for msg in self.__send_request(
                data=data,
                auto_continue=auto_continue,
                timeout=timeout,
        ):
            yield msg

    async def ask(
            self,
            prompt: str,
            conversation_id: str | None = None,
            parent_id: str = "",
            model: str = "",
            auto_continue: bool = False,
            timeout: int = 360,
    ) -> AsyncGenerator[dict, None]:
        """Ask a question to the chatbot

        Args:
            prompt (str): The question to ask
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str, optional): UUID for the message to continue on. Defaults to "".
            model (str, optional): The model to use. Defaults to "".
            auto_continue (bool, optional): Whether to continue the conversation automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.

        Yields:
            AsyncGenerator[dict, None]: The response from the chatbot
            {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str,
                "end_turn": bool,
                "recipient": str,
            }
        """

        messages = [
            {
                "id": str(uuid.uuid4()),
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [prompt]},
            },
        ]

        async for msg in self.post_messages(
                messages=messages,
                conversation_id=conversation_id,
                parent_id=parent_id,
                model=model,
                auto_continue=auto_continue,
                timeout=timeout,
        ):
            yield msg

    async def continue_write(
            self,
            conversation_id: str | None = None,
            parent_id: str = "",
            model: str = "",
            auto_continue: bool = False,
            timeout: float = 360,
    ) -> AsyncGenerator[dict, None]:
        """let the chatbot continue to write
        Args:
            conversation_id (str | None, optional): UUID for the conversation to continue on. Defaults to None.
            parent_id (str, optional): UUID for the message to continue on. Defaults to None.
            model (str, optional): Model to use. Defaults to None.
            auto_continue (bool, optional): Whether to continue writing automatically. Defaults to False.
            timeout (float, optional): Timeout for getting the full response, unit is second. Defaults to 360.


        Yields:
            AsyncGenerator[dict, None]: The response from the chatbot
            {
                "message": str,
                "conversation_id": str,
                "parent_id": str,
                "model": str,
                "finish_details": str,
                "end_turn": bool,
                "recipient": str,
            }
        """
        if parent_id and not conversation_id:
            error = t.Error(
                source="User",
                message="conversation_id must be set once parent_id is set",
                code=t.ErrorType.SERVER_ERROR,
            )
            raise error
        if conversation_id and conversation_id != self.conversation_id:
            self.parent_id = None
        conversation_id = conversation_id or self.conversation_id

        parent_id = parent_id or self.parent_id or ""
        if not conversation_id and not parent_id:
            parent_id = str(uuid.uuid4())
        if conversation_id and not parent_id:
            if conversation_id not in self.conversation_mapping:
                await self.__map_conversations()
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

        async for msg in self.__send_request(
                data=data,
                auto_continue=auto_continue,
                timeout=timeout,
        ):
            yield msg

    async def get_conversations(self, offset: int = 0, limit: int = 20) -> list:
        """
        Get conversations
        :param offset: Integer
        :param limit: Integer
        """
        url = f"{self.base_url}conversations?offset={offset}&limit={limit}"
        response = await self.session.get(url)
        await self.__check_response(response)
        data = json.loads(response.text)
        return data["items"]

    async def get_msg_history(
            self,
            convo_id: str,
            encoding: str | None = "utf-8",
    ) -> dict:
        """
        Get message history
        :param id: UUID of conversation
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = await self.session.get(url)
        if encoding is not None:
            response.encoding = encoding
            await self.__check_response(response)
            return json.loads(response.text)
        return None

    async def gen_title(self, convo_id: str, message_id: str) -> None:
        """
        Generate title for conversation
        """
        url = f"{self.base_url}conversation/gen_title/{convo_id}"
        response = await self.session.post(
            url,
            data=json.dumps(
                {"message_id": message_id, "model": "text-davinci-002-render"},
            ),
        )
        await self.__check_response(response)

    async def change_title(self, convo_id: str, title: str) -> None:
        """
        Change title of conversation
        :param convo_id: UUID of conversation
        :param title: String
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = await self.session.patch(url, data=f'{{"title": "{title}"}}')
        await self.__check_response(response)

    async def delete_conversation(self, convo_id: str) -> None:
        """
        Delete conversation
        :param convo_id: UUID of conversation
        """
        url = f"{self.base_url}conversation/{convo_id}"
        response = await self.session.patch(url, data='{"is_visible": false}')
        await self.__check_response(response)

    async def clear_conversations(self) -> None:
        """
        Delete all conversations
        """
        url = f"{self.base_url}conversations"
        response = await self.session.patch(url, data='{"is_visible": false}')
        await self.__check_response(response)

    async def __map_conversations(self) -> None:
        conversations = await self.get_conversations()
        histories = [await self.get_msg_history(x["id"]) for x in conversations]
        for x, y in zip(conversations, histories):
            self.conversation_mapping[x["id"]] = y["current_node"]

    def __check_fields(self, data: dict) -> bool:
        try:
            data["message"]["content"]
        except (TypeError, KeyError):
            return False
        return True

    async def __check_response(self, response: httpx.Response) -> None:
        # 改成自带的错误处理
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            await response.aread()
            error = t.Error(
                source="OpenAI",
                message=response.text,
                code=response.status_code,
            )
            raise error from e
