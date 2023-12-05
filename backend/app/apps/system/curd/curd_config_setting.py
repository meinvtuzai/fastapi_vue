from sqlalchemy import func
from sqlalchemy.orm import Session

from common.curd_base import CRUDBase
from ..models.config_settings import ConfigSettings
from functools import lru_cache  # 无法缓存curd的函数，因为参数db是动态变化的
from cachetools import cached, TTLCache  # 可以缓存curd的函数，指定里面的key
from core.logger import logger
from core.config import settings

def envkey(*args, key: str):
    return key


class CURDConfigSetting(CRUDBase):

    # @lru_cache(maxsize=8, typed=False)
    @cached(cache=TTLCache(maxsize=10, ttl=settings.CACHE_TTL), key=envkey)
    def getByKey(self, db: Session, key: str) -> dict:
        obj = db.query(*self.query_columns).filter(self.model.key == key, self.model.is_deleted == 0,
                                                   self.model.status.in_((0,))).first()
        logger.info('=========测试缓存是否生效,仅第一次访问无缓存时出现此提示=========')
        if not obj:
            return {}
        return {'key': obj.key, 'name': obj.name, 'value': int(obj.value) if obj.value.isdigit() else obj.value}

    def create(self, db: Session, *, obj_in, creator_id: int = 0):
        res = super().create(db, obj_in=obj_in, creator_id=creator_id)
        self.getByKey.cache_clear()
        logger.info('=========执行创建方法自动清除系统参数缓存=========')
        return res

    def update(self, db: Session, *, _id: int, obj_in, modifier_id: int = 0):
        res = super().update(db, _id=_id, obj_in=obj_in, modifier_id=modifier_id)
        self.getByKey.cache_clear()
        logger.info('=========执行更新方法自动清除系统参数缓存=========')
        return res

    def delete(self, db: Session, *, _id: int, deleter_id: int = 0):
        res = super().delete(db, _id=_id,deleter_id=deleter_id)
        self.getByKey.cache_clear()
        logger.info('=========执行删除方法自动清除系统参数缓存=========')
        return res


curd_config_setting = CURDConfigSetting(ConfigSettings)
