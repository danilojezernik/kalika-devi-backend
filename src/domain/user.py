import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    username: str
    email: str
    full_name: str
    profession: Optional[str] = ''
    technology: Optional[str] = ''
    description: str
    hashed_password: str
    confirmed: bool
    registered: bool
    blog_notification: bool
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
