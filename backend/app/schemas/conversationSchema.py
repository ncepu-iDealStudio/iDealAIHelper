#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:conversationSchema.py
# author:song
# datetime:2023/4/6 19:40
# software: PyCharm

"""
对话接口所需的响应模型
"""
import uuid
import datetime
from pydantic import  BaseModel
from config.enums import  ChatModels


class ConversationSchema(BaseModel):
    id: int = -1
    conversation_id: uuid.UUID = None
    title: str = None
    user_id: int = None
    is_valid: bool = None
    model_name: ChatModels = None
    create_time: datetime.datetime = None
    active_time: datetime.datetime = None

    class Config:
        use_enum_values = True
