from apps.projects.models import Language, WordType, VerbalTense, Word

from apps.projects.schemas.language import LanguageRequest
from apps.projects.schemas.word_type import WordTypeRequest
from apps.projects.schemas.verbal_tense import VerbalTenseRequest
from apps.projects.schemas.words import WordRequest




from core.database import SessionLocal


def handle():
    session = SessionLocal()
    #languages(session)
    #words_types(session)
    #verbal_tense(session)
    words(session)


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

    list_verbal_tense = ['Present', 'Past', 'Future', 'Present Participle', 'Past Participle']

    for verbal_tense in list_verbal_tense:
        data = VerbalTenseRequest(
            value=verbal_tense
        )
        existe = VerbalTense.exists_by_value(session, data.value)
        if not existe:
            VerbalTense.create(session, data)


def words(session):

    list_words = ['Hope', 'Happy', 'Run', 'Eat', 'Drink', 'Go', 'Sad']

    for word in list_words:
        data = WordRequest(
            value=word
        )
        existe = Word.exists_by_value(session, data.value)
        if not existe:
            Word.create(session, data)



handle()