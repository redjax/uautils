from loguru import logger as log
import typing as t

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field


class UACategoryBase(BaseModel):
    client: str
    user_agents: list[str] | None = Field(default_factory=[], repr=False)
    
class UACategoryIn(UACategoryBase):
    pass


class UACategoryOut(UACategoryBase):
    id: int
