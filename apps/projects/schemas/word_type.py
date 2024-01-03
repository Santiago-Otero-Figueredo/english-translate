from pydantic import BaseModel

from typing import Union

class WordTypeRequest(BaseModel):
    value: str

