#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : rule_schemas.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/3

from pydantic import BaseModel


class RuleTypeSchema(BaseModel):
    name: str
    count_num: int
    active: bool = True