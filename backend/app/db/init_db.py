#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : init_db.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/6
import logging
import os

from sqlalchemy.orm import Session
from apps.user.curd.curd_user import curd_user
from apps.permission.curd.curd_role import curd_role
from app.core.config import settings
from apps.permission.models.user import Users
from apps.permission.models.role import Roles
from apps.user.schemas.user_info_schemas import UserCreateSchema
from apps.permission.schemas import RoleSchema
from utils.tools import get_md5
from db.session import engine
import pandas as pd

logger = logging.getLogger(__name__)


def init_users_and_roles(db: Session) -> None:
    users = []
    roles = []
    user = db.query(Users).filter(Users.username == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = UserCreateSchema(
            username=settings.FIRST_SUPERUSER,
            password=get_md5(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            email=settings.FIRST_SUPERUSER_EMAIL
        )
        user = curd_user.create(db=db, obj_in=user_in)
    users.append(user)

    user = db.query(Users).filter(Users.username == settings.SECOND_SUPERUSER).first()
    if not user:
        user_in = UserCreateSchema(
            username=settings.SECOND_SUPERUSER,
            password=get_md5(settings.SECOND_SUPERUSER_EMAIL),
            is_superuser=True,
            email=settings.SECOND_SUPERUSER_PASSWORD
        )
        user = curd_user.create(db=db, obj_in=user_in)
    users.append(user)

    role_dict = {
        'admin': '超级管理员',
        'general': '一般用户',
        'Operation': '管理员',
    }
    for role_key in role_dict.keys():
        role = db.query(Roles).filter(Roles.key == role_key).first()
        if not role:
            role_in = RoleSchema(
                name=role_dict[role_key],
                key=role_key
            )
            role = curd_role.create(db=db, obj_in=role_in)
        roles.append(role)

    if users and roles:
        for user in users:
            user.user_role.extend(roles)
            db.add(user)
            db.commit()


def init_table_data_form_csv(db: Session) -> None:
    init_data_path = os.path.join(os.path.dirname(__file__), "init_data")
    files = ['config_settings.csv', 'dict_data.csv', 'dict_details.csv', 'hiker_developer.csv',
             'hiker_rule.csv', 'hiker_rule_type.csv',
             'menus.csv', 'perm_label.csv', 'perm_label_role.csv', 'role_menu.csv', 'roles.csv',
             'user_role.csv', 'users.csv']
    files.append('login_infor.csv')
    for file in files:
        file_path = os.path.join(init_data_path, settings.SQL_TABLE_PREFIX + file)
        df = pd.read_csv(file_path, sep=",")
        if file == "menus.csv":
            df['component'] = df['component'].apply(lambda x: '' if pd.isnull(x) else x)
            df['name'] = df['name'].apply(lambda x: '' if pd.isnull(x) else x)
        logger.info(f"{file}  load successed")
        table_name = settings.SQL_TABLE_PREFIX + file.replace(".csv", "")
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(df)
        sql = f"ALTER TABLE {table_name} AUTO_INCREMENT = {max(df['id']) + 1 if not df.empty else 1}"
        logger.info(sql)
        db.execute(sql)
    db.commit()
    db.close()


def init_db(session: Session) -> None:
    db = session
    # init_users_and_roles(db) # 纯净模式啥也没有
    init_table_data_form_csv(db)  # demo模式，有数据
