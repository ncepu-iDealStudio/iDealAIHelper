#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    gunicorn启动文件
"""

import os
import sys


def start():
    cmd = 'cd /var/www/test-iDeal-AI-Helper/backend;' \
          '.  /var/www/python_env/testai.quwancode.com/bin/activate;' \
          'pip install -r requirements.txt;' \
          'gunicorn -c deploy/gunicorn.conf main:app -D -k uvicorn.workers.UvicornWorker;'
    os.system(cmd)


def stop():
    cmd = "ps -ef | grep '/var/www/python_env/testai.quwancode.com/bin/gunicorn' | grep -v grep | awk '{print $2}' | xargs kill -9"
    os.system(cmd)


def restart():
    stop()
    start()


if sys.argv[1] == 'start':
    start()
elif sys.argv[1] == 'restart':
    restart()
elif sys.argv[1] == 'stop':
    stop()
else:
    print('params error!')
