#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: ChatDetailModel.py
@time: 2023/4/21 12:40

"""
from typing import Optional

from fastapi_users_db_sqlalchemy import Integer
from sqlalchemy import String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from config.enums import ChatModels
from .baseModel import Base


class ChatDetail(Base):
    """
    ChatGPT 官方 API 所使用的对话详情
    存储对话内容以及响应数据
    """

    __tablename__ = "chat_detail"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_detail_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    chat_id: Mapped[str] = mapped_column(String(36), index=True, unique=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), comment="发起用户id")
    content: Mapped[Optional[str]] = mapped_column(comment="对话内容")
    response: Mapped[Optional[str]] = mapped_column(comment="对话响应")
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否有效")
    is_image: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否是图片")
    create_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None, comment="创建时间")