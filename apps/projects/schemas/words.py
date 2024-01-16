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
    root_word: str
    value: str
    id_word_type: int
    id_verbal_tense: Union[int, None] = None
    translates: List[str]
    examples_json: List[ExampleTranslatesRequest]
