#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views_scheduler.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10
import json
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from common import deps, error_code
from common.sys_schedule import scheduler
from ..curd.curd_job import Job, curd_job as curd
from common.task_apscheduler import query_job_all, query_job_id, modify_job, del_job, cron_pattern
from tasks.demo_task import demo
from common.resp import respSuccessJson, respErrorJson
from common.schemas import StatusSchema
from ...permission.models import Users
from ..schemas import job_schemas

router = APIRouter()

access_name = 'monitor:job'
api_url = '/job'


def get_no_store_res():
    """
    获取所有job|直接从调度器取出，不查数据库
    :return:
    """
    schedules = []
    for job in query_job_all():
        schedules.append(
            {"job_id": job.id, "job_name": job.name, "func_name": job.func_ref, "func_args": job.args,
             "cron_model": str(job.trigger), "coalesce": job.coalesce,
             "next_run": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
             }
        )
    res = {'results': schedules, 'total': len(schedules)}
    return res


@router.get(api_url + '/now', summary="查询当前内存定时任务")
async def get_job_list():
    res = get_no_store_res()
    return respSuccessJson(res)


@router.get(api_url + '/list', summary="查询定时任务调度列表")
async def searchRecords(*,
                        db: Session = Depends(deps.get_db),
                        status: int = Query(None),
                        job_name: str = Query(None),
                        job_group: str = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    res = curd.search(db, job_name=job_name, job_group=job_group, status=status, page=page, page_size=page_size)
    return respSuccessJson(res)


def get_no_store_detail(job_id):
    """
    获取job详情|直接从调度器取出，不查数据库
    :return:
    """
    job = query_job_id(job_id)

    if not job:
        res = {}
    else:
        res = {"job_id": job.id, "job_name": job.name, "func_name": job.func_ref, "func_args": job.args,
               "cron_model": str(job.trigger), "coalesce": job.coalesce,
               "next_run": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
               }
    return res


@router.get(api_url + '/{job_id}', summary="查询定时任务调度详细")
async def get_job_detail(*,
                         db: Session = Depends(deps.get_db),
                         job_id: str = Query(..., title="任务id"),
                         ):
    # res = get_no_store_detail(job_id)
    # if not res:
    #     return respErrorJson(error=error_code.ERROR_TASK_NOT_FOUND)
    # return respSuccessJson(res)

    return respSuccessJson(curd.get(db, _id=int(job_id)))


def create_no_store_job(obj: job_schemas.JobSchema):
    """
    创建job

    简易的任务调度演示 可自行参考文档 https://apscheduler.readthedocs.io/en/stable/
    三种模式
    date: use when you want to run the job just once at a certain point of time
    interval: use when you want to run the job at fixed intervals of time
    cron: use when you want to run the job periodically at certain time(s) of day

    :return:
    """
    job_id = obj.job_id or obj.job_name
    cron_expression = obj.cron_expression
    func_args = obj.func_args
    cron_model = obj.cron_model
    func_name = obj.func_name
    next_run = obj.next_run or datetime.now()
    try:
        func_args = json.loads(func_args)
    except:
        func_args = [job_id]

    res = query_job_id(job_id)
    if res:
        return {"id": res.id, 'error': error_code.ERROR_TASK_INVALID.set_msg(f"{job_id} job already exists")}

    schedule_job = scheduler.add_job(
        func=func_name,
        trigger=cron_model,
        args=func_args,
        id=job_id,  # job ID
        next_run_time=next_run,
        **cron_pattern(cron_expression),
    )
    return {"id": schedule_job.id}


@router.post(api_url, summary="新增定时任务调度")
async def addRecord(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:post"])),
                    obj: job_schemas.JobSchema,
                    ):
    if not obj.next_run:
        obj.next_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res = curd.create(db, obj_in=obj, creator_id=u['id'])
    if res:
        # create_no_store_job(obj)
        return respSuccessJson()
    return respErrorJson(error=error_code.ERROR_TASK_ADD_ERROR)


@router.put(api_url + "/{_id}/status", summary="任务状态修改")
async def setStatus(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:put"])),
                    _id: int,
                    obj: StatusSchema
                    ):
    curd.setStatus(db, _id=_id, status=obj.status, modifier_id=u['id'])
    return respSuccessJson()


@router.put(api_url + "/{_id}", summary="修改定时任务调度")
async def setRecord(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:put"])),
                    _id: int,
                    obj: job_schemas.JobSchema,
                    ):
    curd.update(db, _id=_id, obj_in=obj, modifier_id=u['id'])
    return respSuccessJson()


@router.delete(api_url + "/{_ids}", summary="删除定时任务调度")
async def delRecord(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:delete"])),
                    _ids: str,
                    ):
    _ids = list(map(lambda x: int(x), _ids.split(',')))
    curd.deletes(db, _ids=_ids, deleter_id=u['id'])
    return respSuccessJson()


@router.put(api_url + '/run', summary="定时任务立即执行一次")
async def run_job(
        job_id: str = Body(..., title="job_id", embed=True),
        job_group: str = Body(..., title="job_group", embed=True),
):
    res = query_job_id(job_id)
    if not res:
        return respErrorJson(error_code.ERROR_TASK_NOT_FOUND.set_msg(f"not found job {job_id}"))

    return respSuccessJson()
