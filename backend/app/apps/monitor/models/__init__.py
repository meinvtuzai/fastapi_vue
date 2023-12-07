from db.base_class import Base
from db.session import engine
from .logininfor import LoginInfor

__all__ = ['LoginInfor']

Base.metadata.create_all(engine)
