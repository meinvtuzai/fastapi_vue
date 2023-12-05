from sqlalchemy import func
from sqlalchemy.orm import Session

from common.curd_base import CRUDBase
from ..models.config_settings import ConfigSettings
from functools import lru_cache # 无法缓存curd的函数，因为参数db是动态变化的


class CURDConfigSetting(CRUDBase):

    @lru_cache(maxsize=8, typed=False)
    def getByKey(self, db: Session, key: str) -> dict:
        obj = db.query(*self.query_columns).filter(self.model.key == key, self.model.is_deleted == 0,
                                                   self.model.status.in_((0,))).first()
        print("=============================")
        if not obj:
            return {}
        return {'key': obj.key, 'name': obj.name, 'value': int(obj.value) if obj.value.isdigit() else obj.value}


curd_config_setting = CURDConfigSetting(ConfigSettings)
