#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2023/4/11 14:32
# software: PyCharm

'''
    this is function  description 
'''
import asyncio
import time
import os
from config.globals import config
from app.controller import ChatGPTManagerFactory


from app.middlewares import AccessLoggerMiddleware, StatisticsMiddleware
from httpx import HTTPError

from fastapi import FastAPI, applications
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html

from sqlalchemy import select
from starlette.exceptions import HTTPException as StarletteHTTPException

import utils.store_statistics

import config.globals as g
from config.enums import ChatStatus
from app.models.userModel import User
from app.models.conversationModel import Conversation
from utils.response import CustomJSONResponse, handle_exception_response
from db.database import create_db_and_tables, get_async_session_context
from utils.exceptions import SelfDefinedException
from app.api.routers import users, chatV1, system, status, chatV3
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import setup_logger, get_logger
from utils.proxy import close_reverse_proxy
from app.controller.userController import create_user
from app import api

import dateutil.parser
from app.chatgpt.typings import Error as revChatGPTError

setup_logger()

logger = get_logger(__name__)


# 初始化重定向请求 Swagger UI查看接口文档
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    default_response_class=CustomJSONResponse,
    middleware=[
        Middleware(AccessLoggerMiddleware, format='%(client_addr)s | %(request_line)s | %(status_code)s | %(M)s ms',
                   logger=get_logger("access")),
        Middleware(StatisticsMiddleware)]
)

app.include_router(users.router)
app.include_router(chatV1.router)
app.include_router(chatV3.router)
app.include_router(system.router)
app.include_router(status.router)

origins = [
    "http://localhost",
    "http://localhost:4000",
]

# 解决跨站问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 定义若干异常处理器

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return handle_exception_response(exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return handle_exception_response(exc)


@app.exception_handler(SelfDefinedException)
async def validation_exception_handler(request, exc):
    return handle_exception_response(exc)


@app.exception_handler(revChatGPTError)
async def validation_exception_handler(request, exc):
    return handle_exception_response(exc)


# 运行前
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    logger.info("database initialized")
    g.startup_time = time.time()

    utils.store_statistics.load()

    if config.get("create_initial_admin_user", False):
        await create_user(config.get("initial_admin_username"),
                          "admin",
                          "admin@admin.com",
                          config.get("initial_admin_password"),
                          is_superuser=True)

    if config.get("create_initial_user", False):
        await create_user(config.get("initial_user_username"),
                          "user",
                          "user@user.com",
                          config.get("initial_user_password"),
                          is_superuser=False)

    if not config.get("sync_conversations_on_startup", True):
        return

    # 重置所有用户chat_status
    async with get_async_session_context() as session:
        r = await session.execute(select(User))
        results = r.scalars().all()
        for user in results:
            user.chat_status = ChatStatus.idling
            session.add(user)
        await session.commit()

    # 运行 Proxy Server
    if config.get("run_reverse_proxy", False):
        from utils.proxy import run_reverse_proxy
        run_reverse_proxy()
        await asyncio.sleep(2)  # 等待 Proxy Server 启动

    # 获取 ChatGPT 对话，并同步数据库
    if not config.get("sync_conversations_on_startup", True):
        logger.info("Sync conversations on startup disabled. Jumping...")
        return  # 跳过同步对话
    try:
        logger.debug(f"Using {os.environ.get('CHATGPT_BASE_URL', '<default_bypass>')} as ChatGPT base url")
        result = await ChatGPTManagerFactory.get_chatgpt_manager().get_conversations()
        logger.info(f"Fetched {len(result)} conversations")
        openai_conversations_map = {conv['id']: conv for conv in result}
        async with get_async_session_context() as session:
            r = await session.execute(select(Conversation))
            results = r.scalars().all()

            for conv_db in results:
                openai_conv = openai_conversations_map.get(conv_db.conversation_id, None)
                if openai_conv:
                    # 同步标题
                    if openai_conv["title"] != conv_db.title:
                        conv_db.title = openai_conv["title"]
                        logger.info(f"Conversation {conv_db.conversation_id} title changed: {conv_db.title}")
                        session.add(conv_db)
                    # 同步时间
                    create_time = dateutil.parser.isoparse(openai_conv["create_time"])
                    if create_time != conv_db.create_time:
                        conv_db.create_time = create_time
                        logger.info(
                            f"Conversation {conv_db.conversation_id} created time changed：{conv_db.create_time}")
                        session.add(conv_db)
                    openai_conversations_map.pop(conv_db.conversation_id)
                else:
                    if conv_db.is_valid:  # 若数据库中存在，但 ChatGPT 中不存在，则将数据库中的对话标记为无效
                        conv_db.is_valid = False
                        logger.info(
                            f"Conversation [{conv_db.title}]({conv_db.conversation_id}) is not valid, marked as invalid")
                        session.add(conv_db)

            # 新增对话
            for openai_conv in openai_conversations_map.values():
                new_conv = Conversation(
                    conversation_id=openai_conv["id"],
                    title=openai_conv["title"],
                    is_valid=True,
                    create_time=dateutil.parser.isoparse(openai_conv["create_time"])
                )
                session.add(new_conv)
                logger.info(
                    f"Conversation [{new_conv.title}]({new_conv.conversation_id}) not recorded, added to database")

            await session.commit()
    except revChatGPTError as e:
        logger.error(f"Fetch conversation error (ChatGPTError): {e.source} {e.code}: {e.message}")
        logger.warning("Sync conversations on startup failed!")
    except HTTPError as e:
        logger.error(f"Fetch conversation error (httpx.HTTPError): {str(e)}")
        logger.warning("Sync conversations on startup failed!")
    except Exception as e:
        logger.error(f"Fetch conversation error (unknown): {str(e)}")
        logger.warning("Sync conversations on startup failed!")


# 关闭时
@app.on_event("shutdown")
async def on_shutdown():
    close_reverse_proxy()
    utils.store_statistics.dump()
