from fastapi.routing import APIRouter

from .user import user_api
from .permission import permission_api
from .system import system_api
from .hiker import hiker_api


api_router = APIRouter()

api_router.include_router(user_api, prefix="/user")
api_router.include_router(system_api, prefix="/system")
api_router.include_router(permission_api, prefix="/permission")
api_router.include_router(hiker_api, prefix="/hiker")


__all__ = ['api_router']