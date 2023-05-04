#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: chatDetailSchema.py
@time: 2023/4/23 14:21

"""
from pydantic import BaseModel, validator


class GenImageSchema(BaseModel):
    message: str
    chat_id: str
    number: str | None = None
    size: str | None = None
