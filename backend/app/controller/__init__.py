#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:song
# datetime:2023/4/7 16:20
# software: PyCharm

"""
this is function  description 
"""
from app.controller.chatgptV1Controller import ChatGPTManager
from app.controller.chatgptV3Controller import ChatGPTV3Manager


# chatGPT官方接口工厂方法
class ChatGPTManagerFactory:
    chatgpt_manager = ChatGPTManager()
    chatgptv3_manager = {}

    @classmethod
    def get_chatgpt_manager(cls, api_key: str = None):
        if api_key is None or api_key == "":
            return cls.chatgpt_manager
        else:
            if cls.chatgptv3_manager.get(api_key):
                return cls.chatgptv3_manager[api_key]
            else:
                cls.chatgptv3_manager[api_key] = ChatGPTV3Manager(api_key=api_key)
                return cls.chatgptv3_manager[api_key]