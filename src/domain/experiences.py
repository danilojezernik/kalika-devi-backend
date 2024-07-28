import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Experiences(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    title: str
    stack: str
    framework: str
    programming_language: str
    company: str
    employee: bool
    tasks: str
    company_start: str
    company_end: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
