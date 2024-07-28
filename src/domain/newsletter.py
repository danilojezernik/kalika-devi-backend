import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Newsletter(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    title: str
    content: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
