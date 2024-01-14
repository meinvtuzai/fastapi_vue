#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : view_rules.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2024/1/14

import os
from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from ...permission.models import Users

from common import deps, error_code
from ..curd.curd_rules import curd_vod_rules as curd
from ..models.vod_rules import VodRules

from common.resp import respSuccessJson, respErrorJson

router = APIRouter()

access_name = 'vod:rules'
api_url = '/rules'


@router.get(api_url + '/list', summary="查询源列表")
async def searchRecords(*,
                        db: Session = Depends(deps.get_db),
                        status: int = Query(None),
                        name: str = Query(None),
                        group: str = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    order_bys = [desc(VodRules.modified_time)]
    res = curd.search(db, status=status, name=name, group=group, page=page,
                      page_size=page_size, order_bys=order_bys)
    return respSuccessJson(res)


@router.post(api_url + "/refresh", summary="刷新源")
async def refreshRules(*,
                           u: Users = Depends(deps.user_perm([f"{access_name}:post"])),):
    # 获取项目根目录
    project_dir = os.getcwd()
    spiders_dir = os.path.join(project_dir, 't4/spiders')
    save_path = os.path.join(spiders_dir, '1.py')
    can_save = True
    return respSuccessJson(data={'path': save_path}, msg='刷新成功')
    # if can_save:
    #     with open(save_path, 'wb') as f:
    #         f.write(up_data)
    #     return respSuccessJson(data={'path': save_path}, msg='上传成功')
    # else:
    #     return respErrorJson(error_code.ERROR_TASK_ADD_ERROR.set_msg(f'上传失败:脚本文件{save_path}已存在'))


@router.delete(api_url + "/clear", summary="清空源")
async def clearRecord(*,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm([f"{access_name}:delete"])),
                      ):
    curd.clear(db)
    return respSuccessJson()


@router.delete(api_url + "/{_ids}", summary="删除源")
async def delRecord(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:delete"])),
                    _ids: str,
                    ):
    _ids = list(map(lambda x: int(x), _ids.split(',')))
    curd.removes(db, _ids=_ids)
    return respSuccessJson()
