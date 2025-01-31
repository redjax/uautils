import typing as t

from .models import UACategoryModel

from loguru import logger as log

import db_lib
from loguru import logger as log

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

class UACategoryRepository(db_lib.base.BaseRepository[UACategoryModel]):
    def __init__(self, session: so.Session):
        super().__init__(session, UACategoryModel)
        
    def get_by_id(self, id: int) -> UACategoryModel:
        return self.session.query(UACategoryModel).filter(UACategoryModel.id == id).one_or_none()
