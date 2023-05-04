#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:generate_id.py
# author:song
# datetime:2023/4/25 18:34
# software: PyCharm

class GenerateID(object):

    # uuid生成
    @staticmethod
    def create_uid():
        import uuid
        return str(uuid.uuid1())

    # hashlib+time
    @staticmethod
    def create_hashlib_id():
        import time, hashlib
        m = hashlib.md5(str(time.clock()).encode('utf-8'))
        return m.hexdigest()

    # 根据时间戳+N位随机数生成自定义唯一健
    @staticmethod
    def create_random_id(N=10):
        import datetime
        import random
        random_number = random.sample('0123456789', N)
        return datetime.datetime.now().strftime('%Y%m%d%H%M') + ''.join(random_number)

    # 用户自定义主键生成规则
    @staticmethod
    def create_custom_id():
        pass

