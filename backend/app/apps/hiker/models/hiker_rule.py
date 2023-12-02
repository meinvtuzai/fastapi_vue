#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : hiker_rule.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/2

from sqlalchemy.orm import relationship, backref

from db.base_class import Base
from db import fields


class HikerRuleType(Base):
    """ 海阔规则类型 """
    name = fields.Char(string='分类名称', required=True)
    count_num = fields.Integer(string='数目')
