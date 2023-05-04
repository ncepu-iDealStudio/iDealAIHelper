#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: conversationController.py
@time: 2023/4/23 14:23

"""

from fastapi import Depends
from sqlalchemy import select
from app.controller.userController import current_active_user
from app.models.conversationModel import Conversation
from app.models.userModel import User
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, AuthorityDenyException


async def get_conversation_by_id(conversation_id: str, user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        r = await session.execute(select(Conversation).where(Conversation.conversation_id == conversation_id))
        conversation = r.scalars().one_or_none()
        if conversation is None:
            raise InvalidParamsException("errors.conversationNotFound")
        if not user.is_superuser and conversation.user_id != user.id:
            raise AuthorityDenyException
        return conversation
