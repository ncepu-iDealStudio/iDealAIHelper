#!/usr/bin/env python
# -*- coding:utf-8 -*-


# file:prompt.py
# author:song
# datetime:2023/4/25 16:46
# software: PyCharm
import os
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select

import config.globals as g
from app import User
from app.controller.promptController import get_prompt_by_prompt_id, get_all_parent_prompt, delete_prompt_by_parent_id, \
    add_prompt_by_json_file, add_prompt_by_csv_file
from app.controller.userController import current_super_user, current_active_user
from app.models import Prompt
from app.schemas.promptSchema import UpdatePromptSchema, CreatePromptSchema
from db.database import get_async_session_context
from utils.exceptions import DataBaseException, InvalidParamsException
from utils.generate_id import GenerateID
from utils.logger import get_logger
from utils.response import response, get_http_message

config = g.config
logger = get_logger(__name__)

router = APIRouter()


@router.get("/prompt", tags=["prompt"])
async def get_all_prompt(_user: User = Depends(current_active_user)):
    """
    get all prompt

    :param _user:

    :return:
    """
    try:
        parent_prompt_results = await get_all_parent_prompt()
        son_prompt_results = await get_prompt_by_prompt_id(prompt_id=None)

        parent_results = jsonable_encoder(parent_prompt_results)
        son_results = jsonable_encoder(son_prompt_results)

        results = {
            'parent_result': parent_results,
            'son_result': son_results,
        }
        return response(200, message=get_http_message(200), result=results)
    except Exception as e:
        raise DataBaseException(str(e))


@router.get("/prompt/{prompt_id}", tags=["prompt"])
async def get_prompt_by_id(prompt_id: str, _user: User = Depends(current_active_user)):
    """
    get prompt by prompt_id

    :param prompt_id:

    :param _user:

    :return:
    """
    try:
        prompt_result = await get_prompt_by_prompt_id(prompt_id=prompt_id)

        results = jsonable_encoder(prompt_result)

        return response(200, message=get_http_message(200), result=results)
    except Exception as e:
        raise DataBaseException(str(e))


@router.patch("/prompt/{prompt_id}", tags=["prompt"])
async def update_prompt_by_id(prompt: UpdatePromptSchema, prompt_id: str, _user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == prompt_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        try:
            if prompt.prompt_parent_id is not None:
                target_prompt.prompt_parent_id = prompt.prompt_parent_id
            if prompt.category is not None:
                target_prompt.category = prompt.category
            if prompt.title is not None:
                target_prompt.title = prompt.title
            if prompt.prompt is not None:
                target_prompt.prompt = prompt.prompt
            session.add(target_prompt)
            await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200))


@router.post("/prompt", tags=["prompt"])
async def create_prompt(prompt: CreatePromptSchema, _user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        try:
            active_time = datetime.utcnow()
            prompt_id = GenerateID.create_random_id()
            new_prompt = Prompt(prompt_parent_id=prompt.prompt_parent_id, prompt_id=prompt_id, category=prompt.category,
                                title=prompt.title, prompt=prompt.prompt, create_time=active_time)
            session.add(new_prompt)
            await session.commit()
            result = {
                'prompt_id': prompt_id,
                'prompt_parent_id': prompt.prompt_parent_id
            }
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200), result=result)


@router.delete("/prompt/{prompt_id}", tags=["prompt"])
async def delete_prompt_by_id(prompt_id: str, _user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == prompt_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        try:
            print(target_prompt.prompt_parent_id)
            if (target_prompt.prompt_parent_id == '0'):
                await delete_prompt_by_parent_id(parent_id=prompt_id)
            target_prompt.is_valid = False
            session.add(target_prompt)
            res = await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200), result=res)


@router.post("/prompt/json/{parent_id}", tags=["prompt"])
async def add_prompt_by_json(parent_id: str, _user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == parent_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        # 获取当前目录
        current_dir_path = os.path.dirname(os.path.abspath(__file__))

        # 获取data目录，即当前目录的上两级目录
        parent_dir_path = os.path.dirname(current_dir_path)
        grandparent_dir_path = os.path.dirname(parent_dir_path)
        data_path = os.path.dirname(grandparent_dir_path)

        target_path = data_path + '\data\prompts\\role-prompts.json'
        try:
            res = await add_prompt_by_json_file(target_path, parent_id=target_prompt.prompt_id,
                                                category=target_prompt.category)
        except Exception as e:
            raise DataBaseException(str(e))

    return response(200, message=get_http_message(200), result=res)


@router.post("/prompt/csv/{parent_id}", tags=["prompt"])
async def add_prompt_by_csv(parent_id: str, _user: User = Depends(current_active_user)):
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == parent_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        # 获取当前目录
        current_dir_path = os.path.dirname(os.path.abspath(__file__))

        # 获取data目录，即当前目录的上两级目录
        parent_dir_path = os.path.dirname(current_dir_path)
        grandparent_dir_path = os.path.dirname(parent_dir_path)
        data_path = os.path.dirname(grandparent_dir_path)

        target_path = data_path + '\data\prompts\prompts.csv'
        try:
            res = await add_prompt_by_csv_file(target_path, parent_id=target_prompt.prompt_id,
                                               category=target_prompt.category)
        except Exception as e:
            raise DataBaseException(str(e))

    return response(200, message=get_http_message(200), result=res)
