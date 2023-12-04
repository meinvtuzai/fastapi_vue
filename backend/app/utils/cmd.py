#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cmd.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/4

import os
import shutil
from core.logger import logger
from common.deps import get_db
import traceback


def update_db():
    try:
        db = next(get_db())  # type: SessionLocal
        dt = db.execute("SELECT now() as t;")
        results = dt.fetchall()
        logger.info(results)
        t = results[0][0]
        logger.info(f"===== {dt.rowcount} {t}=====")
    except:
        traceback.print_exc()
    old_dbfile = 'alembic/versions'
    if os.path.exists(old_dbfile):
        logger.info(f'开始删除历史数据库迁移文件:{old_dbfile}')
        # shutil.rmtree(old_dbfile)
        # db.execute('drop table if exists alembic_version')
    else:
        logger.info(f'未找到历史数据库迁移文件:{old_dbfile}')
    cmd = 'alembic revision --autogenerate -m "auto_update" && alembic upgrade head'
    logger.info(f'开始执行cmd:{cmd}')
    result = os.system(cmd)
    logger.info(f'cmd执行结果:{result} 类型:{type(result)}')
    return result == 0
