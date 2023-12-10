#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : job_schemas.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10

from pydantic import BaseModel
from typing import List, Optional


class JobSchema(BaseModel):
    job_id: str = ''
    job_name: str
    func_name: str
    cron_expression: str
    next_run: Optional[str] = None
    func_args: str = ''
    job_group: str = 'setInterval'
    cron_model: str = 'cron'
    coalesce: int = 0
    status: int = 0
    misfire_policy: int = 3
    active: bool = False
