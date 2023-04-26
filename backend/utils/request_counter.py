#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:request_counter.py
# author:song
# datetime:2023/4/12 16:30
# software: PyCharm
import time
from collections import OrderedDict


class RequestCounter:
    """
    用于统计一段时间内的请求计数和请求用户id
    """
    def __init__(self, time_window: int = None, interval: int = None):
        if time_window % interval != 0 or time_window <= 0 or interval <= 0 or time_window < interval:
            raise ValueError("time_window must be a multiple of duration, and both must be positive")
        self.time_window = time_window or 3 * 24 * 60 * 60
        self.interval = interval or 30
        # counter: {timestage: [count, [user_ids]]}
        self.counter: OrderedDict[int, tuple[int, list[int]]] = OrderedDict()

    def count(self, user_id: int=None):
        current_time = time.time()
        current_interval = int(current_time // self.interval)

        # 增加当前时间段的计数
        if current_interval not in self.counter:
            self.counter[current_interval] = [1, [user_id] if user_id else []]
        else:
            if user_id:
                user_ids = set(self.counter[current_interval][1]).union({user_id})
                user_ids = list(user_ids)
            else:
                user_ids = self.counter[current_interval][1]
            self.counter[current_interval] = (self.counter[current_interval][0] + 1, user_ids)

        # 删除过期的时间段
        self.remove_expired_intervals()

    def remove_expired_intervals(self):
        current_time = time.time()
        current_interval = int(current_time // self.interval)
        expired_interval = current_interval - (self.time_window // self.interval)

        keys_to_delete = []
        for key in self.counter:
            if key <= expired_interval:
                keys_to_delete.append(key)
            else:
                break

        for key in keys_to_delete:
            del self.counter[key]

    def __repr__(self):
        return f"TimeCounter(time_window={self.time_window}, duration={self.interval}, counter={self.counter})"

