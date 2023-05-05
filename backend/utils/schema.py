# !/user/bin/env python
# coding=utf-8
# @project : iDeal-AI-Helper
# @author  : chuck
# @file   : schema.py
# @ide    : PyCharm
# @time   : 2023-04-25 16:06:06
'''
schema 数据操作
'''


# import module your need
def schema_to_model(model, schema):
    """
    保存schema参数到model
    """
    for attr, value in schema.dict(exclude_unset=True).items():
        if value is not None:
            setattr(model, attr, value)


