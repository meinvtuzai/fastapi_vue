#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : sys_schedule.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from core.config import settings


class ScheduleCli(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        # 对象 在 @app.on_event("startup") 中初始化
        self._schedule = None

    def init_scheduler(self) -> None:
        """
        初始化 apscheduler
        :return:
        """
        job_stores = {
            'default': SQLAlchemyJobStore(url=settings.getSqlalchemyURL())
        }
        self._schedule = AsyncIOScheduler(jobstores=job_stores)
        self._schedule.start()

    # 使实例化后的对象 赋予apscheduler对象的方法和属性
    def __getattr__(self, name):
        return getattr(self._schedule, name)

    def __getitem__(self, name):
        return self._schedule[name]

    def __setitem__(self, name, value):
        self._schedule[name] = value

    def __delitem__(self, name):
        del self._schedule[name]


# 创建schedule对象
scheduler: AsyncIOScheduler = ScheduleCli()

# 只允许导出 scheduler 实例化对象
__all__ = ["scheduler"]
