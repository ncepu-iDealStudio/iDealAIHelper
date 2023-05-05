#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:userModel.py
# author:song
# datetime:2023/4/6 15:56
# software: PyCharm

from typing import List, Optional

from fastapi_users_db_sqlalchemy import Integer
from sqlalchemy import String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from config.enums import ChatStatus
from .baseModel import Base

class User(Base):
    """
    用户表
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="用户id")
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True, comment="用户名")
    api_key: Mapped[str] = mapped_column(String(64), nullable=True, default=None, comment="api-key值")
    nickname: Mapped[str] = mapped_column(String(64), comment="昵称")
    email: Mapped[str]=mapped_column(String(64), comment="邮箱")
    active_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None, comment="最后活跃时间")

    chat_status: Mapped[ChatStatus] = mapped_column(Enum(ChatStatus), default=ChatStatus.idling, comment="对话状态")
    can_use_paid: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否可以使用paid模型")
    can_use_gpt4: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否可以使用gpt4模型")
    max_conv_count: Mapped[int] = mapped_column(Integer, default=-1, comment="最大对话数量")
    available_ask_count: Mapped[int] = mapped_column(Integer, default=-1, comment="可用的对话次数")
    available_gpt4_ask_count: Mapped[int] = mapped_column(Integer, default=-1, comment="可用的gpt4对话次数")

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    hashed_password: Mapped[str] = mapped_column(String(1024))
    conversations: Mapped[List["Conversation"]] = relationship("Conversation", back_populates="user")
    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="user")
    allow_context: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否允许上下文功能")
    threshold: Mapped[int] = mapped_column(Integer, default=0, comment="历史上下文阈值")
