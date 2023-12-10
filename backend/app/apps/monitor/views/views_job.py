#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views_scheduler.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10


from datetime import datetime

from fastapi import APIRouter, Query, Body

from common import error_code
from common.sys_schedule import scheduler
from tasks.demo_task import demo
from common.resp import respSuccessJson, respErrorJson

router = APIRouter()

access_name = 'monitor:job'
api_url = '/job'


@router.get(api_url+ '/list', summary="获取所有job信息", name="获取所有定时任务")
async def get_scheduled_syncs():
    """
    获取所有job
    :return:
    """
    schedules = []
    for job in scheduler.get_jobs():
        schedules.append(
            {"job_id": job.id, "func_name": job.func_ref, "func_args": job.args, "cron_model": str(job.trigger),
             "next_run": str(job.next_run_time)}
        )

    return respSuccessJson(data=schedules)


@router.get(api_url+'/{job_id}', summary="获取指定的job信息", name="获取指定定时任务")
async def get_target_sync(
        job_id: str = Query(..., title="任务id")
):
    job = scheduler.get_job(job_id=job_id)

    if not job:
        return respErrorJson(error=error_code.ERROR_TASK_NOT_FOUND)

    return respSuccessJson(
        data={"job_id": job.id, "func_name": job.func_ref, "func_args": job.args, "cron_model": str(job.trigger),
              "next_run": str(job.next_run_time)})


@router.put("/job/run", summary="开始job调度", name="启动定时任务")
async def add_job_to_scheduler(
        *,
        seconds: int = Body(120, title="循环间隔时间/秒,默认120s", embed=True),
        job_id: str = Body(..., title="任务id", embed=True),
):
    """
    简易的任务调度演示 可自行参考文档 https://apscheduler.readthedocs.io/en/stable/
    三种模式
    date: use when you want to run the job just once at a certain point of time
    interval: use when you want to run the job at fixed intervals of time
    cron: use when you want to run the job periodically at certain time(s) of day
    :param seconds:
    :param job_id:
    :return:
    """
    res = scheduler.get_job(job_id=job_id)
    if res:
        return respErrorJson(error_code.ERROR_TASK_INVALID.set_msg(f"{job_id} job already exists"))

    schedule_job = scheduler.add_job(demo,
                                    'interval',
                                    args=(job_id,),
                                    seconds=seconds,  # 循环间隔时间 秒
                                    id=job_id,  # job ID
                                    next_run_time=datetime.now()  # 立即执行
                                    )
    return respSuccessJson(data={"id": schedule_job.id})


@router.delete(api_url, summary="移除任务", name="删除定时任务")
async def remove_schedule(
        job_id: str = Body(..., title="job_id", embed=True)
):
    res = scheduler.get_job(job_id=job_id)
    if not res:
        return respErrorJson(error_code.ERROR_TASK_NOT_FOUND.set_msg(f"not found job {job_id}"))

    scheduler.remove_job(job_id)

    return respSuccessJson()