from pydantic import BaseModel


class WordTypeRequest(BaseModel):
    id: int
    value: str
