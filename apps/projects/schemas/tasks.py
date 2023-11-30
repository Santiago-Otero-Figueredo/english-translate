from pydantic import BaseModel

from typing import Union


class CreateTaskRequest(BaseModel):
    name: str
    description: Union[str, None]
    priority: int
    project: int


class CompleteTaskRequest(BaseModel):
    state: int
