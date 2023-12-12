from apps.projects.models import Language

from apps.projects.schemas.language import LanguageRequest

from core.database import SessionLocal


def handle():
    session = SessionLocal()
    languages(session)


def languages(session):

    data = LanguageRequest(
        value='English'
    )
    existe = Language.exists_by_value(session, data.value)
    if not existe:
        Language.create(session, data)


handle()