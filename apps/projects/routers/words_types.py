from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

from apps.projects.models import WordType
from apps.projects.schemas.word_type import WordTypeRequest

from typing import List


templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/words-types',
    tags=['words-types'],
    responses= {404: {'description': 'Not Found'}}
)


@router.get('/list', status_code=status.HTTP_200_OK, name='list-words-types')
async def list_task(session: Session = Depends(get_session)) -> List[WordTypeRequest]:
    try:
        word_types = await WordType.get_all(session)
        return word_types
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching word types")
