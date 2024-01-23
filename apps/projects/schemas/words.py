from pydantic import BaseModel

from typing import Union, List, Dict

class WordRequest(BaseModel):
    value: str

class WordValueRequest(BaseModel):
    id: int
    value: str

class WordRegister(BaseModel):
    id: Union[int, None] = ''
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
    id_example: Union[int, None] = ''
    id_translate: Union[int, None] = ''
    example: str
    translate: str
    description: Union[str, None] = ''



class WordCompleteInfoRegister(BaseModel):
    root_word: WordRegister
    word_classification: WordRegister
    id_word_type: int
    id_verbal_tense: Union[int, None] = None
    translates: List[str]
    examples_json: List[ExampleTranslatesRequest]

class WordSearchRequest(BaseModel):
    id_word_classification: int
    value_word_classification: str
    id_root_word: int
    value_root_word: str
    id_word_type: int
    id_verbal_tense: Union[int, None] = None
    number_of_times_searched: int
    translates: List[TranslationRequest]
    examples_json: List[ExampleRequest]
