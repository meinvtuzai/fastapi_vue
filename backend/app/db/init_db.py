#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : init_db.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/6


from apps.user.curd.curd_user import curd_user as crud
from app.core.config import settings
from apps.permission.models.user import Users
from apps.permission.schemas import UserInitSchema


def init_db(session) -> None:
    # db = next(get_db())  # type: SessionLocal
    db = session
    user = db.query(Users).filter(Users.username == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = UserInitSchema(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            # is_superuser=True,
            phone='1',
            email='1'
        )
        user = crud.create(db=db, obj_in=user_in)

if __name__ == '__main__':
    init_db()