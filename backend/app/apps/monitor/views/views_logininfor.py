#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views_logininfor.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/7


from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from ...permission.models import Users

from common import deps, error_code
from ..curd.curd_logininfor import curd_logininfor as curd

from common.resp import respSuccessJson, respErrorJson

router = APIRouter()

access_name = 'monitor:logininfor'
api_url = '/logininfor'


@router.get(api_url + '/list', summary="获取登录日志")
async def searchRecords(*,
                        db: Session = Depends(deps.get_db),
                        status: int = Query(None),
                        user_name: str = Query(None),
                        ipaddr: str = Query(None),
                        login_time: str = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    res = curd.search(db, user_name=user_name, ipaddr=ipaddr, status=status, login_time=login_time, page=page,
                      page_size=page_size)
    return respSuccessJson(res)
