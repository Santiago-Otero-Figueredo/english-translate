from apps.projects.models import Language, WordType, VerbalTense, Word, WordClassification

from apps.projects.schemas.language import LanguageRequest
from apps.projects.schemas.word_type import WordTypeRequest
from apps.projects.schemas.verbal_tense import VerbalTenseRequest
from apps.projects.schemas.words import WordRequest
from apps.projects.schemas.words_classification import WordClassificationRequest





from core.database import SessionLocal


def handle():
    session = SessionLocal()
    #languages(session)
    #words_types(session)
    #verbal_tense(session)
    #words(session)
    word_classification(session)


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


def word_classification(session):

    list_words = [
        {
            'value': 'Hope',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 1,
            'word_id': 1
        },
        {
            'value': 'Hopeless',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 2,
            'word_id': 1
        },
        {
            'value': 'Hopeful',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 2,
            'word_id': 1
        },
        {
            'value': 'Happy',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 2,
            'word_id': 2
        },
        {
            'value': 'Unhappy',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 2,
            'word_id': 2
        },
        {
            'value': 'Happiness',
            'description': "",
            'number_of_times_searched': 1,
            'word_type_id': 1,
            'word_id': 2
        },
    ]


    for word in list_words:
        data = WordClassificationRequest(
            value= word['value'],
            description= word['description'],
            number_of_times_searched= word['number_of_times_searched'],
            word_type_id= word['word_type_id'],
            word_id= word['word_id']
        )
        existe = WordClassification.exists_by_value(session, data.value)
        if not existe:
            WordClassification.create(session, data)


handle()