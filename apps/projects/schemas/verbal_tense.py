from pydantic import BaseModel

from typing import Union

class VerbalTenseRequest(BaseModel):
    value: str
    description: Union[str, None] = ''

class VerbalTenseValueRequest(BaseModel):
    id: int
    value: str
