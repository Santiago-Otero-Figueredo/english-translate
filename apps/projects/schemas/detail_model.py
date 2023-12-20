from pydantic import BaseModel

from typing import Union

class DetailModelRequest(BaseModel):
    id: int
    value: str
