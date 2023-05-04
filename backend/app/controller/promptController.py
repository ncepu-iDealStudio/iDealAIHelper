#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:promptController.py
# author:song
# datetime:2023/4/25 16:45
# software: PyCharm

"""
this is function  description 
"""
import csv
import json
from datetime import datetime

from sqlalchemy import select


from app.models import Prompt
from db.database import get_async_session_context
from utils.exceptions import InvalidParamsException, DataBaseException
from utils.generate_id import GenerateID


async def get_all_parent_prompt():
    """get all parent prompt
    """
    async with get_async_session_context() as session:
        r = await session.execute(select(Prompt).where(Prompt.prompt_parent_id == 0, Prompt.is_valid == True))
        prompts = r.scalars().all()
        if prompts is None:
            raise InvalidParamsException("errors.promptsNotFound")
        return prompts


async def get_prompt_by_prompt_id(prompt_id: str | None):
    """get prompt by prompt id
    """
    async with get_async_session_context() as session:
        if prompt_id is None:
            r = await session.execute(select(Prompt).where(Prompt.is_valid == True, Prompt.prompt_parent_id != 0))
        if prompt_id is not None:
            r = await session.execute(select(Prompt).where(Prompt.prompt_id == prompt_id, Prompt.is_valid == True,
                                                           Prompt.prompt_parent_id != 0))
        prompts = r.scalars().all()
        if prompts is None:
            raise InvalidParamsException("errors.promptsNotFound")
        return prompts


async def delete_prompt_by_parent_id(parent_id: str | None):
    if parent_id is None:
        raise InvalidParamsException("errors.parentIDErroe")
    async with get_async_session_context() as session:
        r = await session.execute(select(Prompt).where(Prompt.prompt_parent_id == parent_id, Prompt.is_valid == True))
        prompts = r.scalars().all()
        if prompts is None:
            raise InvalidParamsException("errors.promptsNotFound")
        try:
            for prompt in prompts:
                prompt.is_valid = False
                session.add(prompt)
            result = await session.commit()
        except Exception as e:
            raise DataBaseException(str(e))
        return result


async def add_prompt_by_json_file(target_path: str,parent_id:str|None,category:str|None):
    if parent_id is None:
        parent_id=0
    if category is None:
        category='add_by_json'

    with open(target_path, 'r', encoding='utf-8') as f:
        prompts_data = json.load(f)

    async with get_async_session_context() as session:
        prompt_id_list=[]
        prompt_list=[]
        try:
            for dict in prompts_data:
                active_time = datetime.utcnow()
                prompt_id = GenerateID.create_random_id()
                new_prompt = Prompt(prompt_parent_id=parent_id, prompt_id=prompt_id,
                                    category=category,
                                    title=dict['act'], prompt=dict['prompt'], create_time=active_time)
                prompt_list.append(new_prompt)
                prompt_id_list.append(prompt_id)
            session.add_all(prompt_list)
            await session.commit()
            result={
                'prompt_id_list':prompt_id_list,
                'prompt_parent_id':0
            }
        except Exception as e:
            raise DataBaseException(str(e))
        return result

async def add_prompt_by_csv_file(target_path: str,parent_id:str|None,category:str|None):
    if parent_id is None:
        parent_id=0
    if category is None:
        category='add_by_csv'

    prompts_data=[]
    with open(target_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        for row in csv_reader:
            temp_dict={
                'act':row[0],
                'prompt':row[1]
            }
            prompts_data.append(temp_dict)
    async with get_async_session_context() as session:
        prompt_id_list=[]
        prompt_list=[]
        try:
            for dict in prompts_data:
                active_time = datetime.utcnow()
                prompt_id = GenerateID.create_random_id()
                new_prompt = Prompt(prompt_parent_id=parent_id, prompt_id=prompt_id,
                                    category=category,
                                    title=dict['act'], prompt=dict['prompt'], create_time=active_time)
                prompt_list.append(new_prompt)
                prompt_id_list.append(prompt_id)
            session.add_all(prompt_list)
            await session.commit()
            result={
                'prompt_id_list':prompt_id_list,
                'prompt_parent_id':0
            }
        except Exception as e:
            raise DataBaseException(str(e))
        return result

