from pydantic import BaseModel


class Sleep(BaseModel):
    number: int
