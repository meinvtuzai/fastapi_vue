#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/3

from fastapi import APIRouter
from starlette.responses import HTMLResponse, RedirectResponse
from core.config import settings
from utils.web import HtmlSender
from network.request import Request

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
