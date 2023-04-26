#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:userSchema.py
# author:song
# datetime:2023/4/6 19:39
# software: PyCharm
"""
用户接口所需的响应模型
"""
import datetime
from fastapi_users import schemas
from pydantic import BaseModel

from config.enums import ChatStatus


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    nickname: str
    api_key: str | None
    email: str
    active_time: datetime.datetime | None

    chat_status: ChatStatus

    can_use_paid: bool
    can_use_gpt4: bool
    max_conv_count: int | None
    available_ask_count: int | None
    available_gpt4_ask_count: int | None

    is_superuser: bool
    is_active: bool
    is_verified: bool


class UserUpdate(schemas.BaseUser[int]):
    nickname: str
    email: str = None
    api_key: str | None


class UserResetPassword(BaseModel):
    user_id: int
    new_password: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    nickname: str
    api_key: str | None
    email: str
    can_use_paid: bool = False
    max_conv_count: int = -1
    available_ask_count: int = -1

    class Config:
        orm_mode = True


class LimitSchema(BaseModel):
    can_use_paid: bool | None = None
    can_use_gpt4: bool | None = None
    max_conv_count: int | None = None
    available_ask_count: int | None = None
    available_gpt4_ask_count: int | None = None


class AccountSchema(BaseModel):
    api_key: str | None
    can_use_paid: bool | None = None
    can_use_gpt4: bool | None = None
    max_conv_count: int | None = None
    available_ask_count: int | None = None
    available_gpt4_ask_count: int | None = None


class KeySchema(BaseModel):
    api_key: str | None
