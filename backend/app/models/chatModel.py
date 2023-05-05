#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: ChatModel.py
@time: 2023/4/21 10:22

"""
from typing import Optional

from fastapi_users_db_sqlalchemy import Integer
from sqlalchemy import String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from config.enums import ChatModels
from .baseModel import Base


class Chat(Base):
    """
    ChatGPT 官方 API 所使用的对话
    记录对话和用户之间的对应关系，存储内容
    与chatDetail表关联：一对多，一个Chat对应多个ChatDetail
    """

    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String(20),comment="对话标题")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), comment="发起用户id")
    user: Mapped["User"] = relationship(back_populates="chats")
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否有效")
    model_name: Mapped[Optional[Enum["ChatModels"]]] = mapped_column(
        Enum(ChatModels, values_callable=lambda obj: [e.value for e in obj] if obj else None), default=None,
        comment="使用的模型")
    create_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None, comment="创建时间")
    active_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None, comment="最后活跃时间")
