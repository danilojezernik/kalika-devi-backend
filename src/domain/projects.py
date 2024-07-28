"""
Project is ment to show all my work until today. If there is something i did there should be a link to the github
repository if it is public and website link. Here it will also be by category. If beginner there will be projects that i
think are for beginners.

There will be few types:
JavaScript/Typescript
Python/FastAPI
Angular 2
Vue.js
"""

import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Projects(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    title: str
    subtitle: str
    category: str
    content: str
    github: str
    website: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
