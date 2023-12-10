#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : demo_task.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10

from core.logger import logger


def demo(task_id: str):
    print(f'=========task_id:{task_id}=========')
    logger.info("demo_task.py执行一次定时任务......")
