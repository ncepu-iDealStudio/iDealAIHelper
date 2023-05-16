#!/usr/bin/env python
# -*- coding:utf-8 -*-


# file:prompt.py
# author:song
# datetime:2023/4/25 16:46
# software: PyCharm

import os
import time
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy import select

import config.globals as g
from app import User
from app.controller.promptController import get_prompt_by_prompt_id, get_all_parent_prompt, delete_prompt_by_parent_id, \
    add_prompt_by_json_file, add_prompt_by_csv_file, add_prompts_by_xlsx_file, get_prompt_to_file, \
    update_prompt_by_parent_id, get_prompt_by_parent_id
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


@router.get("/prompt/part-prompt", tags=["prompt"])
async def get_prompt_by_id(prompt_id:str=None, prompt_parent_id:str=None,_user: User = Depends(current_active_user)):
    """
    get prompt by prompt_id

    :param prompt_id:

    :param _user:

    :return:
    """
    try:
        if prompt_id is not None:
            prompt_result = await get_prompt_by_prompt_id(prompt_id=prompt_id)
            results = jsonable_encoder(prompt_result)
            return response(200, message=get_http_message(200), result=results)
        if prompt_parent_id is not None:
            prompt_result = await get_prompt_by_parent_id(prompt_parent_id)
            results = jsonable_encoder(prompt_result)
            return response(200, message=get_http_message(200), result=results)
        return response(200, message=get_http_message(200), result={})
    except Exception as e:
        raise DataBaseException(str(e))


@router.patch("/prompt/{prompt_id}", tags=["prompt"])
async def update_prompt_by_id(prompt: UpdatePromptSchema, prompt_id: str, _user: User = Depends(current_super_user)):
    """
    update prompt by id

    :param prompt:

    :param prompt_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == prompt_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        try:
            is_change_category=False

            if prompt.prompt_parent_id is not None:
                target_prompt.prompt_parent_id = prompt.prompt_parent_id

            if prompt.category is not None:
                is_change_category=True
                target_prompt.category = prompt.category

            if prompt.title is not None:
                target_prompt.title = prompt.title

            if prompt.prompt is not None:
                target_prompt.prompt = prompt.prompt

            if target_prompt.prompt_parent_id=="0" and is_change_category:
                res=await update_prompt_by_parent_id(parent_id=target_prompt.prompt_id,category=prompt.category)
            session.add(target_prompt)
            await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200),result=res)


@router.post("/prompt", tags=["prompt"])
async def create_prompt(prompt: CreatePromptSchema, _user: User = Depends(current_super_user)):
    """
    create prompt

    :param prompt:

    :param _user:

    :return:
    """
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
async def delete_prompt_by_id(prompt_id: str, _user: User = Depends(current_super_user)):
    """
    delete prompt by id

    :param prompt_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        res = await session.execute(select(Prompt).where(Prompt.prompt_id == prompt_id, Prompt.is_valid == True))
        target_prompt = res.scalars().one_or_none()
        if target_prompt is None:
            raise InvalidParamsException("errors.promptNotExist")
        try:
            if (target_prompt.prompt_parent_id == '0'):
                await delete_prompt_by_parent_id(parent_id=prompt_id)
            target_prompt.is_valid = False
            session.add(target_prompt)
            res = await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return response(200, message=get_http_message(200), result=res)


@router.post("/prompt/json/{parent_id}", tags=["prompt"])
async def add_prompt_by_json(parent_id: str, _user: User = Depends(current_super_user)):
    """
    add prompt by json file

    :param parent_id:

    :param _user:

    :return:
    """
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

        target_path = data_path + '/data/prompts/role-prompts.json'
        try:
            res = await add_prompt_by_json_file(target_path, parent_id=target_prompt.prompt_id,
                                                category=target_prompt.category)
        except Exception as e:
            raise DataBaseException(str(e))

    return response(200, message=get_http_message(200), result=res)


@router.post("/prompt/csv/{parent_id}", tags=["prompt"])
async def add_prompt_by_csv(parent_id: str, _user: User = Depends(current_super_user)):
    """
    add prompt by csv file

    :param parent_id:

    :param _user:

    :return:
    """
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

        target_path = data_path + '/data/prompts/prompts.csv'
        try:
            res = await add_prompt_by_csv_file(target_path, parent_id=target_prompt.prompt_id,
                                               category=target_prompt.category)
        except Exception as e:
            raise DataBaseException(str(e))

    return response(200, message=get_http_message(200), result=res)


@router.get("/prompt/manager/example_file", tags=["prompt"])
async def download_example_file(_user: User = Depends(current_super_user)):
    """
    download example file to add prompt

    :param _user:

    :return:
    """
    try:
        # 获取当前目录
        current_dir_path = os.path.dirname(os.path.abspath(__file__))

        # 获取data目录，即当前目录的上两级目录
        parent_dir_path = os.path.dirname(current_dir_path)
        grandparent_dir_path = os.path.dirname(parent_dir_path)
        data_path = os.path.dirname(grandparent_dir_path)

        target_path = data_path + '/data/prompts'
        filename = "prompts_example.xlsx"

        file_path = f"{target_path}/{filename}"  # replace with your file path
        return FileResponse(file_path, filename=filename,
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        raise e


@router.post("/prompt/manager/upload", tags=["prompt"])
async def upload_file(file: UploadFile = File(...), _user: User = Depends(current_super_user)):
    """
    upload xlsx file to add prompt

    :param file:

    :param _user:

    :return:
    """
    timestamp = int(time.time())  # 生成时间戳
    filename = f"{timestamp}.xlsx"  # 将时间戳作为文件名

    # 获取当前目录
    current_dir_path = os.path.dirname(os.path.abspath(__file__))

    # 获取data目录，即当前目录的上两级目录
    parent_dir_path = os.path.dirname(current_dir_path)
    grandparent_dir_path = os.path.dirname(parent_dir_path)
    data_path = os.path.dirname(grandparent_dir_path)

    target_path = data_path + '/data/prompts'

    file_path = os.path.join(target_path, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    data = await add_prompts_by_xlsx_file(file_path, filename)

    return {"filename": filename, "data": data}


@router.get("/prompt/manager/all_prompt", tags=["prompt"])
async def download_all_prompt_file(_user: User = Depends(current_super_user)):
    """
    download all prompt from database

    :param _user:

    :return:
    """
    try:
        # 获取当前目录
        current_dir_path = os.path.dirname(os.path.abspath(__file__))

        # 获取data目录，即当前目录的上两级目录
        parent_dir_path = os.path.dirname(current_dir_path)
        grandparent_dir_path = os.path.dirname(parent_dir_path)
        data_path = os.path.dirname(grandparent_dir_path)

        target_path = data_path + '/data/prompts'
        file_path = await get_prompt_to_file(target_path)
        filename = "all_prompts.xlsx"

        # file_path = f"{target_path}/{filename}"  # replace with your file path
        return FileResponse(file_path, filename=filename,
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        raise e
