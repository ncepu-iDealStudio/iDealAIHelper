#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: promptModel.py
@time: 2023/4/23 20:57

"""
from typing import Optional
from .baseModel import Base
from sqlalchemy import String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy import Integer


class Prompt(Base):
    """
    chatgpt提示词
    """
    __tablename__ = "prompt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    prompt_parent_id: Mapped[str] = mapped_column(String(36))
    category: Mapped[str] = mapped_column(String(255), comment="分类")
    title: Mapped[Optional[str]] = mapped_column(String(255), comment="对话标题")
    prompt: Mapped[Optional[str]] = mapped_column(String(5000), comment="提示词")
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否有效")
    create_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None, comment="创建时间")
