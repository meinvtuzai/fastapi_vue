# _*_ coding: utf-8 _*_
"""
@File    : __init__.py
@State   :
@Datetime: 2022/8/29 14:01
@Author  : 离小镜 
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.logger import logger


def demo():
    logger.info("开启定时任务......")


scheduler = AsyncIOScheduler()
scheduler.add_job(func=demo, trigger='interval', seconds=10)

