#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: chatSchema.py
@time: 2023/4/23 14:20

"""
import uuid
import datetime
from pydantic import BaseModel, validator
from config.enums import ChatModels
from utils.exceptions import InvalidParamsException


class ChatSchema(BaseModel):
    id: int = -1
    chat_id: uuid.UUID = None
    title: str = None
    user_id: int = None
    is_valid: bool = None
    model_name: ChatModels = None
    create_time: datetime.datetime = None
    active_time: datetime.datetime = None

    class Config:
        use_enum_values = True


class CreateChatSchema(BaseModel):
    title: str
    model_name: ChatModels
