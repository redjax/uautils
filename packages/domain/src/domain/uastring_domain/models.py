import typing as t

import db_lib

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc
from sqlalchemy.dialects.postgresql import JSONB


class UACategoryModel(db_lib.Base):
    __tablename__ = "ua_categories"
    __table_args__ = (sa.UniqueConstraint("client"),)
    
    id: so.Mapped[db_lib.annotated.INT_PK]
    
    client: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False, unique=True)
    user_agents: so.Mapped[list[str]] = so.mapped_column(sa.JSON, nullable=False, default=list)