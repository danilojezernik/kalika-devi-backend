import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    naslov: str
    podnaslov: str
    tehnologija: str
    vsebina: str
    image: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
