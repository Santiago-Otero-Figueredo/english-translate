from apps.projects.models import Language, WordType, VerbalTense

from apps.projects.schemas.language import LanguageRequest
from apps.projects.schemas.word_type import WordTypeRequest
from apps.projects.schemas.verbal_tense import VerbalTenseRequest



from core.database import SessionLocal


def handle():
    session = SessionLocal()
    #languages(session)
    #words_types(session)
    verbal_tense(session)


def languages(session):

    data = LanguageRequest(
        value='English'
    )
    existe = Language.exists_by_value(session, data.value)
    if not existe:
        Language.create(session, data)


def words_types(session):

    list_types = ['Nouns', 'Adjectives', 'Verbs', 'Adverbs']

    for type in list_types:
        data = WordTypeRequest(
            value=type
        )
        existe = WordType.exists_by_value(session, data.value)
        if not existe:
            WordType.create(session, data)


def verbal_tense(session):

    list_types = ['Present', 'Past', 'Future', 'Present Participle', 'Past Participle']

    for type in list_types:
        data = VerbalTenseRequest(
            value=type
        )
        existe = VerbalTense.exists_by_value(session, data.value)
        if not existe:
            VerbalTense.create(session, data)



handle()