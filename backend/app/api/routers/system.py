import os

from fastapi import APIRouter, Depends
from sqlalchemy import select

import config.enums
import config.globals as g
from app.controller.systemController import read_last_n_lines, check_users

from db.database import get_async_session_context
from app.models.userModel import User
from app.models.conversationModel import Conversation
from app.schemas.systemSchema import LogFilterOptions, SystemInfo, RequestStatistics
from app.controller.userController import current_super_user
from utils.logger import get_logger

config = g.config
logger = get_logger(__name__)

router = APIRouter()


@router.get("/system/info", tags=["system"], response_model=SystemInfo)
async def get_system_info(_user: User = Depends(current_super_user)):
    active_user_in_5m, active_user_in_1h, active_user_in_1d, queueing_count, users = await check_users(
        refresh_cache=True)
    async with get_async_session_context() as session:
        conversations = await session.execute(select(Conversation))
        conversations = conversations.scalars().all()
    result = SystemInfo(
        startup_time=g.startup_time,
        total_user_count=len(users),
        total_conversation_count=len(conversations),
        valid_conversation_count=len([c for c in conversations if c.is_valid]),
    )
    return result


@router.get("/system/request_statistics", tags=["system"], response_model=RequestStatistics)
async def get_request_statistics(_user: User = Depends(current_super_user)):
    result = RequestStatistics(
        request_counts_interval=g.request_log_counter_interval,
        request_counts=dict(g.request_log_counter.counter),
        ask_records=list(g.ask_log_queue.queue)
    )
    return result


@router.post("/system/proxy_logs", tags=["system"])
async def get_proxy_logs(_user: User = Depends(current_super_user), options: LogFilterOptions = LogFilterOptions()):
    lines = read_last_n_lines(
        os.path.join(config.get("log_dir", "logs"), "reverse_proxy.log"),
        options.max_lines,
        options.exclude_keywords
    )
    return lines


@router.post("/system/server_logs", tags=["system"])
async def get_server_logs(_user: User = Depends(current_super_user), options: LogFilterOptions = LogFilterOptions()):
    lines = read_last_n_lines(
        g.server_log_filename,
        options.max_lines,
        options.exclude_keywords
    )
    return lines
