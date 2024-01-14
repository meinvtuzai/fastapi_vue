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

from core.config import settings
from core.logger import logger
from ...permission.models import Users

from common import deps, error_code
from ..curd.curd_rules import curd_vod_rules as curd
from ..models.vod_rules import VodRules

from common.resp import respSuccessJson, respErrorJson
from common.schemas import StatusSchema, ActiveSchema

from pathlib import Path

router = APIRouter()

access_name = 'vod:rules'
api_url = '/rules'


@router.get(api_url + '/list', summary="查询源列表")
async def searchRecords(*,
                        db: Session = Depends(deps.get_db),
                        status: int = Query(None),
                        name: str = Query(None),
                        group: str = Query(None),
                        order_by: str = Query(None),
                        is_desc: bool = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    order_bys = [desc(VodRules.order_num)] if is_desc else [asc(VodRules.order_num)]
    if order_by:
        if order_by == 'created_ts':
            order_bys += [desc(VodRules.created_time)] if is_desc else [asc(VodRules.created_time)]
        elif order_by == 'modified_ts':
            order_bys += [desc(VodRules.modified_time)] if is_desc else [asc(VodRules.modified_time)]
        elif order_by == 'name':
            order_bys += [desc(VodRules.name)] if is_desc else [asc(VodRules.name)]
        elif order_by == 'id':
            order_bys = [desc(VodRules.id)] if is_desc else [asc(VodRules.id)]
        elif order_by == 'order_num':
            order_bys = order_bys

    # print(order_bys)
    res = curd.search(db, status=status, name=name, group=group, page=page,
                      page_size=page_size, order_bys=order_bys)
    return respSuccessJson(res)


@router.post(api_url + "/refresh", summary="刷新源")
async def refreshRules(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm([f"{access_name}:post"])), ):
    # 获取项目根目录
    project_dir = os.getcwd()
    spiders_dir = os.path.join(project_dir, 't4/spiders')
    files = os.listdir(spiders_dir)
    files_data = []
    for file in files:
        fpath = os.path.join(spiders_dir, file)
        fpath = Path(fpath).as_posix()
        # print(fpath)
        name = os.path.basename(fpath)
        base_name, extension = os.path.splitext(name)
        if os.path.isfile(fpath):
            files_data.append({
                'name': base_name,
                'group': extension,
                'path': fpath,
                'is_exist': True,
                'file_type': extension,
            })
    for file_info in files_data:
        record = curd.getByName(db, file_info['name'], file_info['file_type'])
        if record:
            curd.update(db, _id=record.id, obj_in=file_info, modifier_id=u['id'])
        else:
            file_info.update({
                'order_num': 0,
                'ext': '',
                'status': 1,
                'active': True,
            })
            max_order_num = curd.get_max_order_num(db)
            file_info.update({'order_num': max_order_num + 1})
            record = curd.create(db, obj_in=file_info, creator_id=u['id'])
        logger.info(f'record: id:{record.id} name:{record.name}{record.file_type}')

    logger.info(files_data)
    return respSuccessJson(data={'spiders_dir': spiders_dir}, msg='刷新成功')


@router.put(api_url + "/{_id}/active", summary="修改源是否显示")
async def setActive(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm([f"{access_name}:put"])),
                    _id: int,
                    obj: ActiveSchema
                    ):
    curd.setActive(db, _id=_id, active=obj.active, modifier_id=u['id'])
    return respSuccessJson()


@router.delete(api_url + "/clear", summary="清空源")
async def clearRecord(*,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm([f"{access_name}:delete"])),
                      ):
    curd.clear(db)
    table_name = settings.SQL_TABLE_PREFIX + 'vod_rules'
    sql = ''
    if 'mysql' in settings.SQLALCHEMY_ENGINE:
        sql = f"ALTER TABLE {table_name} AUTO_INCREMENT = 1"
    elif 'postgresql' in settings.SQLALCHEMY_ENGINE:
        sql = f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;"
        # sql = f"select setval('{table_name}_id_seq', '1') from {table_name};"
    if sql:
        logger.info(f'执行重置索引的SQL:{sql}')
        db.execute(sql)
        db.commit()
        db.close()
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
