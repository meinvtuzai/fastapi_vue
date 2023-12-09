#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : curd_logininfor.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/2
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func, distinct
from common.curd_base import CRUDBase
from ..models.logininfor import LoginInfor
from network.request import Request


class CURDLoginInfor(CRUDBase):

    # def init(self):
    #     self.query_columns.extend((self.model.dt2ts(self.model.login_time, "login_time_ts"),
    #                                ))
    #     self.exclude_columns.extend((self.model.login_time))  # 排除时间字段

    def create(self, db: Session, *, obj_in, creator_id: int = 0):
        obj_in_data = obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
        # obj_in_data['creator_id'] = creator_id
        ipaddr = obj_in_data.get('ipaddr') or ''
        if ipaddr and not ipaddr.startswith('127.0'):
            #  查询已有的此ip的记录
            logined_record = db.query(LoginInfor).filter(LoginInfor.ipaddr == ipaddr).filter(
                LoginInfor.login_location.isnot(None)).first()
            if logined_record:
                obj_in_data['login_location'] = logined_record.login_location
            else:
                try:
                    ip_url = f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ipaddr}'
                    request = Request(method="GET", url=ip_url, agent=False, follow_redirects=True, timeout=0.5)
                    # 同步
                    r = request.request()
                    resp = r.json()
                    if resp.get('msg') == '查询成功':
                        d = resp['data']
                        prov = d['prov']
                        city = d['city']
                        district = d['district']
                        owner = d['owner']
                        obj_in_data['login_location'] = f'{prov}{city}{district}{owner}'
                except Exception as e:
                    print(f'查询ip归属地发生错误:{e}')
                    pass

        # db_obj = self.model(**obj_in_data)
        db_obj = obj_in_data
        return super().create(db, obj_in=db_obj, creator_id=creator_id)

    def search(self, db: Session, *, user_name: str = "", ipaddr: str = "", status: int = None,
               login_time: str = "", order_bys: Optional[list] = None,
               page: int = 1, page_size: int = 25) -> dict:
        filters = []
        if status is not None:
            filters.append(self.model.status == status)
        if user_name:
            filters.append(self.model.user_name.like(f"%{user_name}%"))
        if ipaddr:
            filters.append(self.model.ipaddr.like(f"%{ipaddr}%"))
        if login_time:
            filters.append(self.model.login_time.like(f"%{login_time}%"))
        # FIXME: 暂不支持开始和结束时间区间查询

        records, total, _, _ = self.get_multi(db, page=page, page_size=page_size, filters=filters, order_bys=order_bys)
        return {'results': records, 'total': total}


curd_logininfor = CURDLoginInfor(LoginInfor)
