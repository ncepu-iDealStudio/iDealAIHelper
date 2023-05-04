import time
import uuid
from datetime import datetime
from typing import List

import httpx
import requests
from fastapi import APIRouter, Depends, WebSocket
from fastapi.encoders import jsonable_encoder
from httpx import HTTPError
from sqlalchemy import select, and_, delete, func

import config.globals as g
from app.controller import ChatGPTManagerFactory
from app.controller.conversationController import get_conversation_by_id
from app.controller.userController import current_active_user, websocket_auth, current_super_user, \
    change_user_chat_status

from app.chatgpt.typings import Error as revChatGPTError
from app.models.chatDetailModel import ChatDetail
from app.models.chatModel import Chat
from app.models.conversationModel import Conversation
from app.models.userModel import User
from app.schemas.conversationSchema import ConversationSchema
from config.enums import ChatStatus, ChatModels
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, AuthorityDenyException, DataBaseException
from utils.logger import get_logger
from utils.response import response, get_http_message

config = g.config
logger = get_logger(__name__)

router = APIRouter()


@router.get("/conv", tags=["conversation"], response_model=List[ConversationSchema])
async def get_all_conversations(user: User = Depends(current_active_user), fetch_all: bool = False):
    """
    Return my active conversations.
    For admin, return all conversations and optionally specify to only return active conversations.

    :param user: current active user

    :param fetch_all:

    :return: conversations List
    """
    if fetch_all and not user.is_superuser:
        raise AuthorityDenyException()

    stat = and_(Conversation.user_id == user.id, Conversation.is_valid)
    if fetch_all:
        stat = None
    async with get_async_session_context() as session:
        if stat is not None:
            r = await session.execute(select(Conversation).where(stat))
        else:
            r = await session.execute(select(Conversation))
        results = r.scalars().all()
        results = jsonable_encoder(results)
        return results


@router.get("/conv/{conversation_id}", tags=["conversation"])
async def get_conversation_history(conversation: Conversation = Depends(get_conversation_by_id)):
    """
    Get historical conversation by conversation_id

    :param conversation:

    :return:
    """
    result = await ChatGPTManagerFactory.get_chatgpt_manager().get_conversation_messages(
        conversation.conversation_id)
    # 当不知道模型名时，顺便从对话中获取
    if conversation.model_name is None:
        model_name = result.get("model_name")
        if model_name is not None and not ChatModels.unknown.value:
            async with get_async_session_context() as session:
                conversation = await session.get(Conversation, conversation.id)
                conversation.model_name = model_name
                session.add(conversation)
                await session.commit()
    return result


@router.delete("/conv/{conversation_id}", tags=["conversation"])
async def delete_conversation(conversation: Conversation = Depends(get_conversation_by_id)):
    """
    remove conversation from database(set is_valid=False) and chatgpt server

    :param conversation:

    :return:
    """
    if not conversation.is_valid:
        raise InvalidParamsException("errors.conversationAlreadyDeleted")
    try:
        await ChatGPTManagerFactory.get_chatgpt_manager().delete_conversation(conversation.conversation_id)
    except revChatGPTError as e:
        logger.warning(f"delete conversation {conversation.conversation_id} failed: {e.code} {e.message}")
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 404:
            raise e
    async with get_async_session_context() as session:
        conversation.is_valid = False
        session.add(conversation)
        await session.commit()
    return response(200)


@router.delete("/conv/{conversation_id}/vanish", tags=["conversation"])
async def vanish_conversation(conversation: Conversation = Depends(get_conversation_by_id)):
    """
    remove conversation from database and chatgpt server

    :param conversation:

    :return:
    """
    if conversation.is_valid:
        try:
            await ChatGPTManagerFactory.get_chatgpt_manager().delete_conversation(conversation.conversation_id)
        except revChatGPTError as e:
            logger.warning(f"delete conversation {conversation.conversation_id} failed: {e.code} {e.message}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 404:
                raise e
    async with get_async_session_context() as session:
        await session.execute(delete(Conversation).where(Conversation.conversation_id == conversation.conversation_id))
        await session.commit()
    return response(200)


@router.patch("/conv/{conversation_id}", tags=["conversation"], response_model=ConversationSchema)
async def change_conversation_title(title: str, conversation: Conversation = Depends(get_conversation_by_id)):
    """
    change conversation's title by conversation_id

    :param title: new title

    :param conversation: target conversation

    :return:

    """
    await ChatGPTManagerFactory.get_chatgpt_manager().set_conversation_title(conversation.conversation_id,
                                                                             title)
    async with get_async_session_context() as session:
        conversation.title = title
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
    result = jsonable_encoder(conversation)
    return result


@router.patch("/conv/{conversation_id}/assign/{username}", tags=["conversation"])
async def assign_conversation(username: str, conversation_id: str, _user: User = Depends(current_super_user)):
    """
    assign conversation for user

    :param username:

    :param conversation_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        user = await session.execute(select(User).where(User.username == username))
        user = user.scalars().one_or_none()
        if user is None:
            raise InvalidParamsException("errors.userNotFound")
        conversation = await session.execute(
            select(Conversation).where(Conversation.conversation_id == conversation_id))
        conversation = conversation.scalars().one_or_none()
        if conversation is None:
            raise InvalidParamsException("errors.conversationNotFound")
        conversation.user_id = user.id
        session.add(conversation)
        await session.commit()
    return response(200)


@router.patch("/conv/{conversation_id}/gen_title", tags=["conversation"], response_model=ConversationSchema)
async def generate_conversation_title(message_id: str, conversation: Conversation = Depends(get_conversation_by_id)):
    """
    generate title for conversation

    :param message_id:

    :param conversation:

    :return:
    """
    if conversation.title is not None:
        raise InvalidParamsException("errors.conversationTitleAlreadyGenerated")
    async with get_async_session_context() as session:
        result = await ChatGPTManagerFactory.get_chatgpt_manager().generate_conversation_title(conversation.id,
                                                                                               message_id)
        if result["title"]:
            conversation.title = result["title"]
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
        else:
            raise InvalidParamsException(f"{result['message']}")
    result = jsonable_encoder(conversation)
    return result


@router.websocket("/conv")
async def ask(websocket: WebSocket):
    """
    Updating ChatGPT responses in real-time using WebSocket.

    When a client connects for the first time, send { message, conversation_id?, parent_id?, use_paid?, timeout? }
    conversation_id = null for new session, otherwise response to the message specified by parent_id.

    The server responds with: { type, tip, message, conversation_id, parent_id, use_paid, title }
   "type" can be "waiting" / "message" / "title".
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
    conversation_id = params.get("conversation_id", None)
    parent_id = params.get("parent_id", None)
    model_name = params.get("model_name")
    # timeout = params.get("timeout", 30)  # default 30s
    timeout = config.get("ask_timeout", 300)
    new_title = params.get("new_title", None)

    if message is None:
        await websocket.close(1007, "errors.missingMessage")
        return
    if parent_id is not None and conversation_id is None:
        await websocket.close(1007, "errors.missingConversationId")
        return

    is_new_conv = conversation_id is None
    conversation = None
    if not is_new_conv:
        conversation = await get_conversation_by_id(conversation_id, user)
        model_name = model_name or conversation.model_name
    else:
        model_name = model_name or ChatModels.default

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
            select(func.count(Conversation.id)).filter(and_(Conversation.user_id == user.id, Conversation.is_valid)))
        user_chats_count = user_chats_count.scalar()
        if is_new_conv and user.max_conv_count != -1 and user_chats_count >= user.max_conv_count:
            await websocket.close(1008, "errors.maxConversationCountReached")
            return
        if user.available_ask_count != -1 and user.available_ask_count <= 0:
            await websocket.close(1008, "errors.noAvailableAskCount")
            return
        if user.available_gpt4_ask_count != -1 and user.available_gpt4_ask_count <= 0 and model_name == ChatModels.gpt4:
            await websocket.close(1008, "errors.noAvailableGPT4AskCount")
            return

    if ChatGPTManagerFactory.get_chatgpt_manager().is_busy():
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
        async with ChatGPTManagerFactory.get_chatgpt_manager().semaphore:
            await change_user_chat_status(user.id, ChatStatus.asking)
            await websocket.send_json({
                "type": "waiting",
                "tip": "tips.waiting"
            })
            ask_start_time = time.time()
            try:
                # 调用chatgpt_manager的ask方法提问
                async for data in ChatGPTManagerFactory.get_chatgpt_manager().ask(message, conversation_id,
                                                                                  parent_id, timeout, model_name):
                    reply = {
                        "type": "message",
                        "message": data["message"],
                        "conversation_id": data["conversation_id"],
                        "parent_id": data["parent_id"],
                        "model_name": data["model"],
                    }
                    # print(data['message'])
                    await websocket.send_json(reply)
                    # 新对话时保存conversation_id方便下次连续对话
                    if conversation_id is None:
                        conversation_id = data["conversation_id"]
            except Exception as e:
                # 修复 message 为 None 时的错误
                if str(e).startswith("Field missing"):
                    logger.warning(str(e))
                else:
                    logger.error(e)
                    raise e
            finally:
                ask_stop_time = time.time()

                logger.debug(
                    f"finish ask {conversation_id} ({model_name}), reply using : {ask_stop_time - ask_start_time}s")

            async with get_async_session_context() as session:
                # 若新建了对话，则添加到数据库
                if is_new_conv and conversation_id is not None:
                    # 设置默认标题
                    try:
                        if new_title is not None:
                            await ChatGPTManagerFactory.get_chatgpt_manager().set_conversation_title(
                                conversation_id, new_title)
                    except Exception as e:
                        logger.warning(e)
                    finally:
                        current_time = datetime.utcnow()
                        conversation = Conversation(conversation_id=conversation_id, title=new_title, user_id=user.id,
                                                    model_name=model_name, create_time=current_time,
                                                    active_time=current_time)
                        session.add(conversation)
                # 更新 conversation
                if not is_new_conv:
                    conversation = await session.get(Conversation, conversation.id)  # 此前的 conversation 属于另一个session
                    conversation.active_time = datetime.utcnow()
                    if conversation.model_name != model_name:
                        conversation.model_name = model_name
                    session.add(conversation)

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
        ChatGPTManagerFactory.get_chatgpt_manager().reset_chat()
        await websocket.close(websocket_code, websocket_reason)
        stop_time = time.time()

        # 写入到 scope 中，供统计
        g.ask_log_queue.enqueue(
            (user.id, model_name.value, ask_stop_time - ask_start_time, stop_time - start_time))
