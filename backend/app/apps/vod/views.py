#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : views.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/7
import base64
import json

from fastapi import APIRouter, Request, Depends, Response, Query, File, UploadFile
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
# @router.get(api_url + "/{api:path}", summary="生成Vod")
@router.api_route(methods=['GET', 'POST'], path=api_url + "/{api:path}", summary="生成Vod")
def vod_generate(*, api: str = "", request: Request,
                 db: Session = Depends(deps.get_db),
                 ) -> Any:
    """
    通过动态import的形式，统一处理vod:爬虫源T4接口
    ext参数默认为空字符串，传入api配置里对应的ext，可以是文本和链接
    """

    def getParams(key=None, value=''):
        return request.query_params.get(key) or value

    # 拿到query参数的字典
    params_dict = request.query_params.__dict__['_dict']
    # 拿到网页host地址
    host = request.base_url
    # 拼接字符串得到t4_api本地代理接口地址
    api_url = str(request.url).split('?')[0]
    t4_api = f'{api_url}?proxy=true&do=py'

    try:
        vod = Vod(api=api, query_params=request.query_params, t4_api=t4_api).module
    except Exception as e:
        return respErrorJson(error_code.ERROR_INTERNAL.set_msg(f"内部服务器错误:{e}"))

    ac = getParams('ac')
    ids = getParams('ids')
    filters = getParams('f')  # t1 筛选 {'cid':'1'}
    ext = getParams('ext')  # t4筛选传入base64加密的json字符串
    api_ext = getParams('api_ext')  # t4初始化api的扩展参数
    extend = getParams('extend')  # t4初始化配置里的ext参数
    filterable = getParams('filter')  # t4能否筛选
    if request.method.lower() == 'POST'.lower():  # t4 ext网络数据太长会自动post,此时强制可筛选
        filterable = True
    wd = getParams('wd')
    quick = getParams('quick')
    play_url = getParams('play_url')  # 类型为t1的时候播放链接带这个进行解析
    play = getParams('play')  # 类型为4的时候点击播放会带上来
    flag = getParams('flag')  # 类型为4的时候点击播放会带上来
    t = getParams('t')
    pg = getParams('pg', '1')
    pg = int(pg)
    q = getParams('q')

    # 本地代理所需参数
    proxy = getParams('proxy')
    do = getParams('do')

    extend = extend or api_ext
    vod.setExtendInfo(extend)

    # 获取依赖项
    depends = vod.getDependence()
    modules = []
    module_names = []
    for lib in depends:
        try:
            module = Vod(api=lib, query_params=request.query_params, t4_api=t4_api).module
            modules.append(module)
            module_names.append(lib)
        except Exception as e:
            logger.info(f'装载依赖{lib}发生错误:{e}')
            # return respErrorJson(error_code.ERROR_INTERNAL.set_msg(f"内部服务器错误:{e}"))

    if len(module_names) > 0:
        logger.info(f'当前依赖列表:{module_names}')

    vod.init(modules)

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

    if proxy and do == 'py':
        try:
            back_resp_list = vod.localProxy(params_dict)
            status_code = back_resp_list[0]
            media_type = back_resp_list[1]
            content = back_resp_list[2]
            if isinstance(content, str):
                content = content.encode('utf-8')
            return Response(status_code=status_code, media_type=media_type, content=content)
        except Exception as e:
            error_msg = f"localProxy执行发生内部服务器错误:{e}"
            logger.error(error_msg)
            return respErrorJson(error_code.ERROR_INTERNAL.set_msg(error_msg))

    if play:  # t4播放
        try:
            play_url = vod.playerContent(flag, play, vipFlags=None)
            if isinstance(play_url, str):
                return respVodJson({'parse': 0, 'playUrl': '', 'jx': 0, 'url': play_url})
            elif isinstance(play_url, dict):
                return respVodJson(play_url)
            else:
                return play_url
        except Exception as e:
            error_msg = f"playerContent执行发生内部服务器错误:{e}"
            logger.error(error_msg)
            return respErrorJson(error_code.ERROR_INTERNAL.set_msg(error_msg))

    if play_url:  # t1播放
        play_url = vod.playerContent(flag, play_url, vipFlags=None)
        if isinstance(play_url, str):
            return RedirectResponse(play_url, status_code=301)
        elif isinstance(play_url, dict):
            return respVodJson(play_url)
        else:
            return play_url

    if ac and t:  # 一级
        try:
            fl = {}
            if filters and filters.find('{') > -1 and filters.find('}') > -1:
                fl = json.loads(filters)
            # print(filters,type(filters))
            # print(fl,type(fl))
            logger.info(fl)
            data = vod.categoryContent(t, pg, filterable, fl)
            return respVodJson(data)
        except Exception as e:
            error_msg = f"categoryContent执行发生内部服务器错误:{e}"
            logger.error(error_msg)
            return respErrorJson(error_code.ERROR_INTERNAL.set_msg(error_msg))

    if ac and ids:  # 二级
        try:
            id_list = ids.split(',')
            data = vod.detailContent(id_list)
            return respVodJson(data)
        except Exception as e:
            error_msg = f"detailContent执行发生内部服务器错误:{e}"
            logger.error(error_msg)
            return respErrorJson(error_code.ERROR_INTERNAL.set_msg(error_msg))
    if wd:  # 搜索
        try:
            data = vod.searchContent(wd, quick, pg)
            return respVodJson(data)
        except Exception as e:
            error_msg = f"searchContent执行发生内部服务器错误:{e}"
            logger.error(error_msg)
            return respErrorJson(error_code.ERROR_INTERNAL.set_msg(error_msg))

    home_data = vod.homeContent(filterable)
    home_video_data = vod.homeVideoContent()
    home_data.update(home_video_data)

    return respVodJson(home_data)
