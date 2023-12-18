from pydantic import BaseModel

from typing import Union

class WordRequest(BaseModel):
    value: str

class WordValueRequest(BaseModel):
    id: int
    value: str
