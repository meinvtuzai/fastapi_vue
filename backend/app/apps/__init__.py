from fastapi.routing import APIRouter

from .user import user_api
from .permission import permission_api
from .system import system_api
from .hiker import hiker_developer_api, hiker_rule_type_api

api_router = APIRouter()

api_router.include_router(user_api, prefix="/user", tags=["用户管理"])
api_router.include_router(system_api, prefix="/system", tags=["系统设置"])
api_router.include_router(permission_api, prefix="/permission", tags=["权限管理"])

hiker_apis = [hiker_developer_api, hiker_rule_type_api]
for hiker_api in hiker_apis:
    api_router.include_router(hiker_api, prefix="/hiker", tags=["海阔视界"])

__all__ = ['api_router']
