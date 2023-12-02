from db.base_class import Base
from db.session import engine
from .hiker_developer import HikerDeveloper


__all__ = ['HikerDeveloper']


Base.metadata.create_all(engine)