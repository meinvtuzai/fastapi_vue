import os

from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from utils.encrypt import get_uuid
from ..permission.models import Users
from .schemas import developer_schemas
from .curd.curd_hiker_developer import curd_hiker_developer

from common import deps, error_code

from common.resp import respSuccessJson, respErrorJson

from core import constants

router = APIRouter()

@router.get("/hiker_developer", summary="搜索开发者")
async def searchRecords(*,
                        db: Session = Depends(deps.get_db),
                        status: int = Query(None),
                        name: str = Query(None),
                        qq: str = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    res = curd_hiker_developer.search(db, name=name, qq=qq, status=status, page=page, page_size=page_size)
    return respSuccessJson(res)


@router.get("/hiker_developer/{_id}", summary="通过ID获取开发者信息")
async def getRecord(*,
                       db: Session = Depends(deps.get_db),
                       _id: int,
                       ):
    return respSuccessJson(curd_hiker_developer.get(db, _id=_id))


@router.post("/hiker_developer", summary="添加开发者")
async def addRecord(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["hiker:developer:post"])),
                       obj: developer_schemas.DeveloperSchema,
                       ):
    res = curd_hiker_developer.create(db, obj_in=obj, creator_id=u['id'])
    if res:
        return respSuccessJson()
    return respErrorJson(error=error_code.ERROR_USER_PREM_ADD_ERROR)


@router.put("/hiker_developer/{_id}", summary="修改开发者")
async def setRecord(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["hiker:developer:put"])),
                       _id: int,
                       obj: developer_schemas.DeveloperSchema,
                       ):
    curd_hiker_developer.update(db, _id=_id, obj_in=obj, updater_id=u['id'])
    return respSuccessJson()


@router.delete("/hiker_developer/{_id}", summary="删除开发者")
async def delRecord(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["hiker:developer:delete"])),
                       _id: int,
                       ):
    curd_hiker_developer.delete(db, _id=_id, deleter_id=u['id'])
    return respSuccessJson()

@router.put("/hiker_developer/{_id}/is_manager", summary="修改开发者是否为超管")
async def setIsManager(*,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm(["hiker:developer:put"])),
                     _id: int,
                    obj: developer_schemas.IsManagerSchema
                      ):
    curd_hiker_developer.setIsManager(db, id=_id, is_manager=obj.is_manager, modifier_id=u['id'])
    return respSuccessJson()

@router.put("/hiker_developer/{_id}/active", summary="修改开发者是否启用")
async def setActive(*,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm(["hiker:developer:put"])),
                     _id: int,
                    obj: developer_schemas.ActiveSchema
                      ):
    curd_hiker_developer.setActive(db, id=_id, active=obj.active, modifier_id=u['id'])
    return respSuccessJson()
