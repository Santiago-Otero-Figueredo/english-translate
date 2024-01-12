from pydantic import BaseModel

from typing import Union, List, Dict

class WordRequest(BaseModel):
    value: str

class WordValueRequest(BaseModel):
    id: int
    value: str

class ExampleTranslatesRequest(BaseModel):
    example: str
    translate: str

class WordRegister(BaseModel):
    rootWord: str
    value: str
    idWordTypesSelect: int
    verbalTense: Union[int, None] = None
    translates: List[str]
    examplesJson: List[ExampleTranslatesRequest]
