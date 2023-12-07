#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : curd_logininfor.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/2

from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func, distinct
from common.curd_base import CRUDBase
from ..models.logininfor import LoginInfor


class CURDLoginInfor(CRUDBase):

    def search(self, db: Session, *, user_name: str = "", ipaddr: str = "", status: int = None,
               login_time: str = "",
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
        records, total, _, _ = self.get_multi(db, page=page, page_size=page_size, filters=filters)
        return {'results': records, 'total': total}


curd_logininfor = CURDLoginInfor(LoginInfor)
