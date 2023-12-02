#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : fields.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/2

import sqlalchemy as sql
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from core.config import settings

NONE = 'null'
# NONE = None

def now():
    return func.now()


def today():
    return func.current_date()

def text(any):
    if type(any) == bool:
        any_str = str(int(any))
    else:
        any_str = str(any)
    return sql.text(any_str)

def Char(string: str, default=NONE, required=False, length=256):
    return Column(sql.String(length), default=default, server_default=text(default), nullable=not required,
                  comment=string)


def Boolean(string: str, default=False, required=False):
    return Column(sql.Boolean, default=default, server_default=text(default), nullable=not required, comment=string)


def Float(string: str, default=0.00, required=False):
    return Column(sql.Float, default=default, server_default=text(default), nullable=not required, comment=string)


def Integer(string: str, default=0, required=False):
    return Column(sql.Integer, default=default, server_default=text(default), nullable=not required, comment=string)


def Date(string: str, default=NONE, required=False):
    return Column(sql.Date, default=default, server_default=text(default), nullable=not required, comment=string)


def Datetime(string: str, default=NONE, required=False):
    return Column(sql.DateTime, default=default, server_default=text(default), nullable=not required, comment=string)


def Many2one(comodel_name, string='', default=NONE, required=False, ondelete='set null'):
    return Column(sql.Integer,
                  ForeignKey(f"{settings.SQL_TABLE_PREFIX}{comodel_name}.id", default=default,
                             server_default=text(default), nullable=not required, comment=string, ondelete=ondelete))
