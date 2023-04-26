#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: chatV3.py
@time: 2023/4/23 14:18

"""
import time
import uuid
from datetime import datetime

import requests
from fastapi import APIRouter, Depends, WebSocket
from fastapi.encoders import jsonable_encoder
from httpx import HTTPError
from sqlalchemy import select, and_, func

import config.globals as g
from app.api.routers.chatV1 import change_user_chat_status
from app.chatgpt.typings import Error as revChatGPTError
from app.controller import ChatGPTManagerFactory
from app.controller.chatController import get_chat_by_id
from app.controller.chatDetailController import get_chat_details_by_chat_id, delete_chat_by_id
from app.controller.userController import current_active_user, websocket_auth
from app.models.chatDetailModel import ChatDetail
from app.models.chatModel import Chat
from app.models.userModel import User
from app.schemas.chatSchema import CreateChatSchema
from config.enums import ChatStatus, ChatModels
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, AuthorityDenyException, DataBaseException
from utils.logger import get_logger
from utils.response import response, get_http_message

config = g.config
logger = get_logger(__name__)

router = APIRouter()


# 获取chat列表
@router.get("/chat", tags=["chat"])
async def get_all_chat( _user: User = Depends(current_active_user)):
    """get chat lists of current User

    :param _user: current User

    :return: list of chats
    """
    stat = and_(Chat.user_id == _user.id, Chat.is_valid)
    async with get_async_session_context() as session:
        if stat is not None:
            r = await session.execute(select(Chat).where(stat))
        else:
            r = await session.execute(select(Chat))
        results = r.scalars().all()
        results = jsonable_encoder(results)
        return results


# 添加chat会话
@router.post("/chat/{user_id}/new_chat/", tags=["chat"])
async def add_chat(createChatSchema: CreateChatSchema, user_id: int = None, _user: User = Depends(current_active_user)):
    """add a new chat

    :param createChatSchema: schema of a new chat

    :param user_id: user id

    :param _user: current User

    :return: Response
    """
    async with get_async_session_context() as session:
        target_user: User = await session.get(User, user_id)
        if target_user is None:
            raise InvalidParamsException("errors.userNotExist")
        # 创建chat_id
        chat_id = str(uuid.uuid1())
        add_dict = {
            'chat_id': chat_id,
            'user_id': user_id,
            'title': createChatSchema.title,
            'model_name': createChatSchema.model_name,
            'is_valid': 1
        }
        from app.models.chatModel import Chat
        new_conv = Chat(**add_dict)
        result = {
            'chat_id': chat_id,
        }
        try:
            session.add(new_conv)
            await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))

        return response(200, message=get_http_message(200), result=result)


# 删除chat会话
@router.delete("/chat/{chat_id}", tags=["chat"])
async def delete_chat(chat_id:str=None, _user: User = Depends(current_active_user)):
    """delete a chat

    :param chat_id: id of the chat

    :param _user: current User

    :return: Response
    """
    if chat_id is None:
        raise InvalidParamsException("errors.witoutParsms")
    async with get_async_session_context() as session:
        user_id = _user.id
        res = await session.execute(select(Chat).where(Chat.chat_id == chat_id, Chat.user_id == user_id))
        target_chat = res.scalars().one_or_none()
        if target_chat is None:
            raise InvalidParamsException("errors.chatNotExist")
        try:
            target_chat.is_valid = False
            await session.commit()
            await delete_chat_by_id(chat_id=chat_id)
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200))

# 获取chat会话历史信息
@router.get("/chat/{chat_id}", tags=["chat"])
async def get_chat_history(chat_id: str, user: User = Depends(current_active_user)):
    """get history of a chat

    :param chat_id: id of the chat

    :param _user: current User

    :return: Response
    """
    async with get_async_session_context() as session:
        r = await session.execute(select(ChatDetail).where(ChatDetail.chat_id == chat_id))
        chats = r.scalars().all()
        if chats is None:
            raise InvalidParamsException("errors.chatsNotFound")
        for chat_detail in chats:
            if not user.is_superuser and chat_detail.user_id != user.id:
                raise AuthorityDenyException
        result = jsonable_encoder(chats)
        return response(200, get_http_message(200), result)


# 更新chat标题
@router.patch("/chat/{chat_id}/new_title/{chat_title}", tags=["chat"])
async def update_chat_title(chat_id: str, chat_title: str, user: User = Depends(current_active_user)):
    """update chat title

    :param chat_id: id of a chat

    :param chat_title: title of a chat

    :param _user: current User

    :return: Response
    """
    async with get_async_session_context() as session:
        user_id = user.id
        res = await session.execute(select(Chat).where(Chat.chat_id == chat_id, Chat.user_id == user_id))
        target_chat = res.scalars().one_or_none()
        if target_chat is None:
            raise InvalidParamsException("errors.chatNotExist")
        try:
            target_chat.title = chat_title
            result = await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200), result=result)


# chat会话
@router.websocket("/chat")
async def chat(websocket: WebSocket):
    """
    利用 WebSocket 实时更新 ChatGPT 回复.

    客户端第一次连接：发送 { message, chat_id, model_name, ask_timeout }
        chat_id 为空则新建会话，否则回复 chat_id 指定的消息
    服务端返回格式：{ type, message, chat_id, chat_detail_id, model_name }
    其中：type 可以为 "waiting" / "message" / "title"
    """

    start_time = time.time()
    await websocket.accept()
    user = await websocket_auth(websocket)
    logger.debug(f"{user.username} connected to websocket")
    websocket.scope["auth_user"] = user

    if user is None:
        await websocket.close(1008, "errors.unauthorized")
        return

    if user.chat_status != ChatStatus.idling:
        await websocket.close(1008, "errors.cannotConnectMoreThanOneClient")
        return

    # 读取用户输入
    params = await websocket.receive_json()
    message = params.get("message", None)
    chat_id = params.get("chat_id", None)
    model_name = params.get("model_name", "gpt-3.5-turbo")
    timeout = config.get("ask_timeout", 300)

    if message is None:
        await websocket.close(1007, "errors.missingMessage")
        return
    if user.api_key is None:
        await websocket.close(1007, "errors.missingApiKey")
        return

    chatgpt_manager = ChatGPTManagerFactory.get_chatgpt_manager(api_key=f"{user.api_key}")

    is_new_conv = chat_id is None
    chat_info = None
    chat_details = None
    chat_detail_id = str(uuid.uuid4())
    if not is_new_conv:
        chat_info = await get_chat_by_id(chat_id, user)
        chat_details = await get_chat_details_by_chat_id(chat_id, user)
        model_name = model_name or chat_info.model_name
    else:
        model_name = model_name or "gpt-3.5-turbo"

    if isinstance(model_name, str):
        model_name = ChatModels(model_name)
    if model_name == ChatModels.paid and not user.can_use_paid:
        await websocket.close(1007, "errors.userNotAllowToUsePaidModel")
        return
    if model_name == ChatModels.gpt4 and not user.can_use_gpt4:
        await websocket.close(1007, "errors.userNotAllowToUseGPT4Model")
        return
    if model_name in [ChatModels.gpt4, ChatModels.paid] and not config.get("chatgpt_paid", False):
        await websocket.close(1007, "errors.paidModelNotAvailable")
        return

    # 判断是否能新建对话，以及是否能继续提问
    async with get_async_session_context() as session:
        user_chats_count = await session.execute(
            select(func.count(Chat.id)).filter(and_(Chat.user_id == user.id, Chat.is_valid)))
        user_chats_count = user_chats_count.scalar()
        if user.max_conv_count != -1 and user_chats_count >= user.max_conv_count:
            await websocket.close(1008, "errors.maxConversationCountReached")
            return
        if user.available_ask_count != -1 and user.available_ask_count <= 0:
            await websocket.close(1008, "errors.noAvailableAskCount")
            return
        if user.available_gpt4_ask_count != -1 and user.available_gpt4_ask_count <= 0 and model_name == ChatModels.gpt4:
            await websocket.close(1008, "errors.noAvailableGPT4AskCount")
            return

    if chatgpt_manager.is_busy():
        await websocket.send_json({
            "type": "waiting",
            "tip": "tips.queueing"
        })

    websocket_code = 1001
    websocket_reason = "tips.terminated"

    try:
        # 标记用户为 queueing
        await change_user_chat_status(user.id, ChatStatus.queueing)
        # 改变用户对话状态
        async with chatgpt_manager.semaphore:
            await change_user_chat_status(user.id, ChatStatus.asking)
            await websocket.send_json({
                "type": "waiting",
                "tip": "tips.waiting"
            })
            ask_start_time = time.time()
            try:
                # 处理历史对话数据，输入对话上下文
                chat_history = []
                if chat_details:
                    for chat_detail in chat_details:
                        chat_history.append({
                            'content': chat_detail.content,
                            'role': "user"
                        })
                        chat_history.append({
                            'content': chat_detail.response,
                            'role': "assistant"
                        })
                    chatgpt_manager.load_chats(messages=chat_history, chat_id=chat_id)

                # 调用chatgpt_manager的ask方法提问
                async for data in chatgpt_manager.ask(message,
                                                      chat_id=chat_id,
                                                      timeout=timeout,
                                                      model_name=model_name):
                    reply = {
                        "type": "message",
                        "message": data,
                        "chat_id": chat_id,
                        "chat_detail_id": chat_detail_id,
                        "model_name": model_name.value,
                    }

                    await websocket.send_json(reply)
            except Exception as e:
                # 修复 message 为 None 时的错误
                if str(e).startswith("Field missing"):
                    logger.warning(str(e))
                else:
                    logger.error(f"chat err:{e}")
                    raise e
            finally:
                ask_stop_time = time.time()

                logger.debug(
                    f"finish ask {chat_id} ({model_name}), reply using : {ask_stop_time - ask_start_time}s")

            async with get_async_session_context() as session:
                # 若新建了对话，则添加到数据库
                if is_new_conv:
                    # chat_id 存在 添加chat_detail数据
                    if chat_id is not None:
                        try:
                            current_time = datetime.utcnow()
                            chat_detail_model = ChatDetail(chat_detail_id=chat_detail_id, chat_id=chat_id,
                                                           user_id=user.id,
                                                           content=message, response=data, create_time=current_time,
                                                           )
                            session.add(chat_detail_model)
                        except Exception as e:
                            logger.warning(e)
                    # chat_id 不存在，添加chat与chat_detail
                    else:
                        try:
                            current_time = datetime.utcnow()
                            chat_model = Chat(chat_id=chat_id, title=message, user_id=user.id, model_name=model_name,
                                              create_time=current_time, active_time=current_time)
                            session.add(chat_model)
                            chat_detail_model = ChatDetail(chat_detail_id=chat_detail_id, chat_id=chat_id,
                                                           user_id=user.id,
                                                           content=message, response=data, create_time=current_time,
                                                           )
                            session.add(chat_detail_model)
                        except Exception as e:
                            logger.warning(e)

                # 更新 chat
                else:
                    current_time = datetime.utcnow()
                    chats = await session.get(Chat, chat_info.id)  # 此前的 conversation 属于另一个session
                    chats.active_time = current_time
                    if chats.model_name != model_name:
                        chats.model_name = model_name
                    session.add(chats)
                    chat_detail_model = ChatDetail(chat_detail_id=chat_detail_id, chat_id=chat_id,
                                                   user_id=user.id,
                                                   content=message, response=data, create_time=current_time,
                                                   )
                    session.add(chat_detail_model)

                # 扣除一次对话次数
                # 这里的逻辑是：available_ask_count 是总的对话次数，available_gpt4_ask_count 是 GPT4 的对话次数
                # 如果都有限制，则都要扣除一次
                # 如果 available_ask_count 不限但是 available_gpt4_ask_count 限制，则只扣除 available_gpt4_ask_count
                if user.available_ask_count != -1 or user.available_gpt4_ask_count != -1:
                    user = await session.get(User, user.id)
                    if user.available_ask_count != -1:
                        assert user.available_ask_count > 0
                        user.available_ask_count -= 1
                    if model_name == ChatModels.gpt4 and user.available_gpt4_ask_count != -1:
                        assert user.available_gpt4_ask_count > 0
                        user.available_gpt4_ask_count -= 1
                    session.add(user)
                await session.commit()

            websocket_code = 1000
            websocket_reason = "tips.finished"
            logger.debug(reply)
    except requests.exceptions.Timeout:
        await websocket.send_json({
            "type": "error",
            "tip": "errors.timeout"
        })
        websocket_code = 1001
        websocket_reason = "errors.timout"
    except revChatGPTError as e:
        await websocket.send_json({
            "type": "error",
            "tip": "errors.chatgptResponseError",
            "message": f"{e.source} {e.code}: {e.message}"
        })
        websocket_code = 1001
        websocket_reason = "errors.chatgptResponseError"
    except HTTPError as e:
        logger.error(str(e))
        await websocket.send_json({
            "type": "error",
            "tip": "errors.httpError",
            "message": str(e)
        })
        websocket_code = 1014
        websocket_reason = "errors.httpError"
    except Exception as e:
        logger.error(str(e))
        await websocket.send_json({
            "type": "error",
            "tip": "errors.unknownError",
            "message": str(e)
        })
        websocket_code = 1011
        websocket_reason = "errors.unknownError"
    finally:
        await change_user_chat_status(user.id, ChatStatus.idling)
        # chatgpt_manager.clear_conversations()
        await websocket.close(websocket_code, websocket_reason)
        stop_time = time.time()

        # 写入到 scope 中，供统计
        g.ask_log_queue.enqueue(
            (user.id, model_name.value, ask_stop_time - ask_start_time, stop_time - start_time))


@router.get("/token", tags=["token count"])
async def get_token(api_key: str, chat_id: str):
    """get token_count

    :param api_key: api_key

    :param chat_id: chat_id of a chat

    :return: json object
    """
    chatgpt_manager = ChatGPTManagerFactory.get_chatgpt_manager(api_key)
    token_count = chatgpt_manager.chatbot.get_token_count(chat_id)
    max_token = chatgpt_manager.chatbot.get_max_tokens(chat_id)
    message = {
        "token_count": token_count,
        "max_token": max_token
    }
    return jsonable_encoder(message)


@router.get("/verify", tags=["chat"])
async def verify(user: User = Depends(current_active_user)):
    """verify api_key to check whether the api_key is valid.

    :param user: current User

    :return: Response
    """
    if user.api_key:
        res_code = await ChatGPTManagerFactory.get_chatgpt_manager(api_key=f"{user.api_key}").verify_api_key()
        if res_code == 200:
            return response(200, message="认证成功", result="认证成功")
        else:
            return response(4001, "认证失败，请检查api_key", result="认证失败，请检查api_key")
    else:
        return response(4001, "认证失败，请检查api_key", result="认证失败，请检查api_key")

