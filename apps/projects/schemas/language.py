from pydantic import BaseModel

from typing import Union

class LanguageRequest(BaseModel):
    value: str
    description: Union[str, None] = ''
