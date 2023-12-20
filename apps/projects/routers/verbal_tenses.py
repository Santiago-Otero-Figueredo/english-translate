from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

from apps.projects.models import VerbalTense
from apps.projects.schemas.detail_model import DetailModelRequest

from typing import List


templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/verbal-tenses',
    tags=['verbal-tenses'],
    responses= {404: {'description': 'Not Found'}}
)


@router.get('/list', status_code=status.HTTP_200_OK, name='list-verbal-tenses')
async def list_task(session: Session = Depends(get_session)) -> List[DetailModelRequest]:
    try:
        verbal_tenses = await VerbalTense.get_all(session)
        return verbal_tenses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching word types")
