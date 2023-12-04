#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/3

from fastapi import APIRouter
from starlette.responses import HTMLResponse, RedirectResponse

from common import error_code
from core.config import settings
from utils.web import HtmlSender
from utils.cmd import update_db
from network.request import Request
from common.resp import respSuccessJson, respErrorJson
from .schemas import database_schemas

router = APIRouter()
htmler = HtmlSender()
htmler.template_path = settings.WEB_TEMPLATES_DIR


@router.get("/", summary="网站首页")
async def web_home():
    html = htmler.renderTemplate('index')
    return HTMLResponse(html)


@router.get('/favicon.ico', summary="网站默认图标")  # 设置icon
async def favicon():
    return RedirectResponse('/static/img/favicon.svg')


@router.get('/baidu', summary="访问百度")
async def baidu():
    # url = "https://www.iesdouyin.com/web/api/v2/user/info?sec_uid=MS4wLjABAAAAc4BIGF22ZcPBMtc73GAKSf-vEiPWKTLC3RJA423NK_E"
    url = "https://www.baidu.com"
    request = Request(method="GET", url=url, agent=False, follow_redirects=True)
    r = await request.fetch()
    # print(r.text)
    return HTMLResponse(r.text)


@router.put('/database_update', summary="数据库升级")
async def database_update(obj: database_schemas.updateSchema):
    if obj.auth_code == settings.DATABASE_UPDATE_AUTH:
        if update_db():
            return respSuccessJson()
        return respErrorJson(error=error_code.ERROR_DATABASE_CMD_ERROR)
    else:
        return respErrorJson(error=error_code.ERROR_DATABASE_AUTH_ERROR)
