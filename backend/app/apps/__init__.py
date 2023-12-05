from fastapi.routing import APIRouter

from .user import user_api
from .permission import permission_api
from .system import system_api
from .hiker import hiker_developer_api, hiker_rule_type_api, hiker_rule_api
from .monitor import monitor_server_api
from .web import web_api

api_router = APIRouter()
web_router = APIRouter()

api_router.include_router(user_api, prefix="/user", tags=["用户管理"])
api_router.include_router(system_api, prefix="/system", tags=["系统设置"])
api_router.include_router(permission_api, prefix="/permission", tags=["权限管理"])
api_router.include_router(monitor_server_api, prefix="/monitor", tags=["监视器"])

hiker_apis = [hiker_developer_api, hiker_rule_type_api, hiker_rule_api]
for hiker_api in hiker_apis:
    api_router.include_router(hiker_api, prefix="/hiker", tags=["海阔视界"])

web_router.include_router(web_api, prefix="", tags=["网页"])

__all__ = ['api_router']
