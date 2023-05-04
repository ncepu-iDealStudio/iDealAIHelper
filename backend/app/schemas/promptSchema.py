#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:promptSchema.py
# author:song
# datetime:2023/4/25 17:58
# software: PyCharm
from pydantic import BaseModel


class UpdatePromptSchema(BaseModel):
    prompt_parent_id: str | None = None
    category: str | None = None
    title: str | None = None
    prompt: str | None = None

class CreatePromptSchema(BaseModel):
    prompt_parent_id: str
    category: str
    title: str
    prompt: str