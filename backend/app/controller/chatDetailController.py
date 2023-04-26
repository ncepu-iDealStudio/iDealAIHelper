#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: chatDetailController.py
@time: 2023/4/23 14:24

"""

from fastapi import Depends
from sqlalchemy import select

from app.controller.userController import current_active_user
from app.models.chatDetailModel import ChatDetail
from app.models.userModel import User
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, AuthorityDenyException, DataBaseException


async def get_chat_details_by_chat_id(chat_id: str, user: User = Depends(current_active_user)):
    """get ChatDetails by chat_id

    :param chat_id: chat_id to get
    :param user: current user
    :return: List[ChatDetail]
    """
    async with get_async_session_context() as session:
        r = await session.execute(select(ChatDetail).where(ChatDetail.chat_id == chat_id))
        chats = r.scalars().all()
        if chats is None:
            raise InvalidParamsException("errors.chatsNotFound")
        for chat_detail in chats:
            if not user.is_superuser and chat_detail.user_id != user.id:
                raise AuthorityDenyException
        return chats


async def delete_chat_by_id(chat_id: str, user: User = Depends(current_active_user)):
    """delete ChatDetails by chat_id

    :param chat_id: chat_id to delete
    :param user: current user
    """
    async with get_async_session_context() as session:
        r = await session.execute(select(ChatDetail).where(ChatDetail.chat_id == chat_id))
        chats = r.scalars().all()
        if chats is None:
            raise InvalidParamsException("errors.chatsNotFound")
        try:
            for chat_detail in chats:
                chat_detail.is_valid = False
                session.add(chat_detail)
            result = await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return result
