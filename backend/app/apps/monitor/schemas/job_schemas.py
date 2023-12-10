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
    job_group: str = 'setInterval'
    func_name: str
    func_args: str = ''
    cron_model: str = 'interval'
    coalesce: str
    next_run: Optional[str] = None
    cron_expression: str
    status: int = 0
    misfire_policy: int = 3
