#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:time_queue.py
# author:song
# datetime:2023/4/12 16:31
# software: PyCharm
import time
from collections import  deque
from typing import Deque

class TimeQueue:
    def __init__(self, time_window: int):
        self.time_window = time_window
        self.queue: Deque[tuple[any, float]] = deque()    # (item, time)

    def enqueue(self, item):
        current_time = time.time()
        self.queue.append((item, current_time))
        self.dequeue_expired()

    def dequeue_expired(self):
        current_time = time.time()
        while self.queue and self.queue[0][1] < current_time - self.time_window:
            self.queue.popleft()

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return f"TimeQueue(time_window={self.time_window}, data={self.queue}...)"
