from pydantic import BaseModel

from typing import Union

class WordClassificationRequest(BaseModel):
    value: str
    description: Union[str, None] = ""
    number_of_times_searched: int
    word_type_id: int
    word_id: int


class WordClassificationRegister(BaseModel):
    value: str
    number_of_times_searched: int
    word_type_id: int
    word_id: int

class WordClassificationValueRequest(BaseModel):
    id: int
    value: str
