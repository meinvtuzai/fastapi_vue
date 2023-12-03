#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : rule_schemas.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Authors Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/3

from pydantic import BaseModel


class RuleTypeSchema(BaseModel):
    name: str
    count_num: int
    active: bool = True
    
class RuleSchema(BaseModel):
    name: str
    type_id: int
    dev_id: int
    value: str
    url: str
    state: int
    auth: str
    auth_date_time: int
    time_over: bool = False
    b64_value: str
    home_url: str
    pic_url: str
    is_json: bool = True
    is_redirect: bool = False
    is_tap: bool = False
    can_discuss: bool = True
    is_json_list: bool = False
    data_type: int
    version: str
    author: str
    note: str
    good_num: int
    bad_num: int
    reply_num: int
    is_safe: bool = True
    is_good: bool = False
    is_white: bool = False
    not_safe_note: str
    last_active: int