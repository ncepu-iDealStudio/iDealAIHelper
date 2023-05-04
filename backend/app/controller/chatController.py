#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: chatController.py
@time: 2023/4/23 14:24

"""

from fastapi import Depends
from sqlalchemy import select

from app.controller.userController import current_active_user
from app.models.chatModel import Chat
from app.models.userModel import User
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, AuthorityDenyException


async def get_chat_by_id(chat_id: str, user: User = Depends(current_active_user)):
    """get Chat info by chat_id

    :param chat_id: id of the chat
    :param user: current user
    :return: Chat
    """

    async with get_async_session_context() as session:
        r = await session.execute(select(Chat).where(Chat.chat_id == chat_id))
        chat_info = r.scalars().one_or_none()
        if chat_info is None:
            raise InvalidParamsException("errors.conversationNotFound")
        if not user.is_superuser and chat_info.user_id != user.id:
            raise AuthorityDenyException
        return chat_info

