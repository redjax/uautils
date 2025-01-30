from loguru import logger as log
import typing as t

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field


class UAPageScrapeBase(BaseModel):
    category: str
    url: str
    user_agents: list[str] | None = Field(default_factory=[], repr=False)
    
class UAPageScrapeIn(UAPageScrapeBase):
    pass


class UAPageScrapeOut(UAPageScrapeBase):
    id: int
