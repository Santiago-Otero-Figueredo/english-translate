from pydantic import BaseModel

from typing import Union, List, Dict

class WordRequest(BaseModel):
    value: str

class WordValueRequest(BaseModel):
    id: int
    value: str

class TranslationRequest(BaseModel):
    id: int
    value: str
    description: Union[str, None] = ''

class ExampleRequest(BaseModel):
    id: int
    value: str
    translation: TranslationRequest

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

class WordSearchRequest(BaseModel):
    id: int
    value: str
    id_root_word: int
    id_word_type: int
    id_verbal_tense: Union[int, None] = None
    number_of_times_searched: int
    translates: List[TranslationRequest]
    examples_json: List[ExampleRequest]
