import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Subscriber(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    name: str
    surname: str
    email: str
    confirmed: bool = False
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
