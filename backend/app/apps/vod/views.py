#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/7
import base64
import json

from fastapi import APIRouter, Request, Depends, Query, File, UploadFile
from fastapi.responses import RedirectResponse
from typing import Any
from sqlalchemy.orm import Session

from .gen_vod import Vod
from common import error_code
from common.resp import respVodJson, respErrorJson
from apps.permission.models.user import Users

from common import deps
from core.logger import logger

router = APIRouter()

access_name = 'vod:generate'
api_url = ''


# u: Users = Depends(deps.user_perm([f"{access_name}:get"]))
@router.get(api_url + "/{api}", summary="生成Vod")
def vod_generate(*, api: str = "", request: Request,
                 db: Session = Depends(deps.get_db),
                 ) -> Any:
    """
    通过动态import的形式，统一处理vod:爬虫源T4接口
    ext参数默认为空字符串，传入api配置里对应的ext，可以是文本和链接
    """

    def getParams(key=None, value=''):
        return request.query_params.get(key) or value

    try:
        vod = Vod(api=api, query_params=request.query_params).module
    except Exception as e:
        return respErrorJson(error_code.ERROR_INTERNAL.set_msg(f"内部服务器错误:{e}"))

    ac = getParams('ac')
    ids = getParams('ids')
    filters = getParams('f')  # t1 筛选 {'cid':'1'}
    ext = getParams('ext')  # t4筛选传入base64加密的json字符串
    api_ext = getParams('api_ext')  # t4初始化api的扩展参数
    extend = getParams('extend')  # t4初始化配置里的ext参数
    filterable = getParams('filter')  # t4能否筛选
    wd = getParams('wd')
    quick = getParams('quick')
    play_url = getParams('play_url') # 类型为t1的时候播放链接带这个进行解析
    play = getParams('play')  # 类型为4的时候点击播放会带上来
    flag = getParams('flag')  # 类型为4的时候点击播放会带上来
    t = getParams('t')
    pg = getParams('pg', '1')
    pg = int(pg)
    q = getParams('q')

    extend = extend or api_ext
    if extend:
        vod.init(extend)

    if ext and not ext.startswith('http'):
        try:
            # ext = json.loads(base64.b64decode(ext).decode("utf-8"))
            filters = base64.b64decode(ext).decode("utf-8")
        except Exception as e:
            logger.error(f'解析发生错误:{e}。未知的ext:{ext}')

    # rule_title = vod.getName().encode('utf-8').decode('latin1')
    rule_title = vod.getName()
    if rule_title:
        logger.info(f'加载爬虫源:{rule_title}')

    if play:  # t4播放
        play_url = vod.playerContent(flag, play, vipFlags=None)
        if isinstance(play_url, str):
            return respVodJson({'parse': 0, 'playUrl': '', 'jx': 0, 'url': play_url})
        elif isinstance(play_url, dict):
            return respVodJson(play_url)
        else:
            return play_url

    if play_url:  # t1播放
        play_url = vod.playerContent(flag, play_url, vipFlags=None)
        if isinstance(play_url, str):
            return RedirectResponse(play_url, status_code=301)
        elif isinstance(play_url, dict):
            return respVodJson(play_url)
        else:
            return play_url

    if ac and t:  # 一级
        fl = {}
        if filters and filters.find('{') > -1 and filters.find('}') > -1:
            fl = json.loads(filters)
        # print(filters,type(filters))
        # print(fl,type(fl))
        logger.info(fl)
        data = vod.categoryContent(t, pg, filterable, fl)
        return respVodJson(data)
    if ac and ids:  # 二级
        id_list = ids.split(',')
        data = vod.detailContent(id_list)
        return respVodJson(data)
    if wd:  # 搜索
        data = vod.searchContent(wd, quick)
        return respVodJson(data)

    home_data = vod.homeContent(filterable)
    home_video_data = vod.homeVideoContent()
    home_data.update(home_video_data)

    return respVodJson(home_data)
