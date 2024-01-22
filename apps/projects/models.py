from sqlalchemy import CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import get_session

from typing import TYPE_CHECKING, List, Union

from datetime import datetime

from .decorators.register import db_transaction
from ..base import DetailModel, BaseModel


####################################### REVISAR ###########################################
# revisar bien este comando para asi saber si evita el reguistro de datos aunque si falla en algun punto de un metodo
# try:
#     session.commit()
#     print("Registro exitoso.")
# except Exception as e:
#     print(f"Error al registrar el verbo: {e}")
#     session.rollback()
# finally:
#     session.close()


class Language(DetailModel):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[Union[str, None]]

    translations: Mapped[List['Translation']] = relationship(back_populates='language')


    @staticmethod
    @db_transaction
    def create(session, data):
        new_register = Language(value=data.value)
        session.add(new_register)
        session.commit()
        session.refresh(new_register)


class WordType(DetailModel):
    __tablename__ = "word_type"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_classifications: Mapped[List['WordClassification']] = relationship(back_populates='word_type')


    @staticmethod
    @db_transaction
    def create(session, data):
        new_register = WordType(value=data.value)
        session.add(new_register)
        session.commit()
        session.refresh(new_register)





class Word(DetailModel):
    __tablename__ = "word"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_classifications: Mapped[List['WordClassification']] = relationship(back_populates='word')

    @staticmethod
    @db_transaction
    def create(session, data):
        new_register = Word(value=data.value)
        session.add(new_register)
        session.commit()
        session.refresh(new_register)

    @staticmethod
    @db_transaction
    async def register_word_with_translates(session, data):
        from apps.projects.schemas.words import WordRegister
        from apps.projects.schemas.words_classification import WordClassificationRegister

        word_type_verb = await WordType.get_by_value(session, 'Verbs')

        # Crear y añadir la palabra
        word = await Word.get_by_value(session, data.root_word)

        if not word:
            # Si la palabra no existe, crear y añadir una nueva
            word = Word(value=data.root_word)
            session.add(word)
            session.commit()

        word_type = await WordType.get_by_id(session, data.id_word_type)

        if not word_type:
            raise Exception('The word type doesn`t exist')
        


        if data.id_verbal_tense:
            verbal_tense = await VerbalTense.get_by_id(session, data.id_verbal_tense)
            if not verbal_tense:
                raise Exception('The verbal tense doesn`t exist')

        word_classification = await WordClassification.get_by_value(session, data.value)

        if not word_classification:
            if word_type_verb.id == word_type_verb.id:
                word_classification = Verb(
                    value=data.value,
                    number_of_times_searched=1,
                    word_type_id=word_type.id,
                    verbal_tense_id=data.id_verbal_tense,
                    word_id=word.id
                )
            else:
                word_classification = WordClassification(
                    value=data.value,
                    number_of_times_searched=1,
                    word_type_id=word_type.id,
                    word_id= word.id
                )
            session.add(word_classification)
            session.commit()
        else:
            word_classification.number_of_times_searched = word_classification.number_of_times_searched + 1 

        session.commit()

        language = await Language.get_by_value(session, 'English')
        # Añadir traducciones
        for translate in data.translates:
            new_translation = Translation(value=translate, word_classification_id=word_classification.id, language_id=language.id)
            session.add(new_translation)
            session.commit()

        # Añadir ejemplos y sus traducciones
        for example_translation in data.examples_json:
            new_example = Example(value=example_translation.example, word_classification_id=word_classification.id)
            session.add(new_example)
            session.commit()
            session.refresh(new_example)
            new_translation = Translation(value=example_translation.translate, description=example_translation.description, word_classification_id=word_classification.id, example_id=new_example.id, language_id=language.id)
            session.add(new_translation)
            session.commit()


        session.commit()


class Example(DetailModel):
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_classification_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))
    word_classification: Mapped['WordClassification'] = relationship(back_populates='examples')

    translation: Mapped['Translation'] = relationship(back_populates='example')

class Translation(DetailModel):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[Union[str, None]]

    word_classification_id: Mapped[Union[int, None]] = mapped_column(ForeignKey('word_classification.id'))
    word_classification: Mapped[Union['WordClassification', None]] = relationship(back_populates='translations')

    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'))
    language: Mapped['Language'] = relationship(back_populates='translations')

    example_id: Mapped[Union[int, None]] = mapped_column(ForeignKey('example.id'))
    example: Mapped[Union['Example', None]] = relationship(back_populates='translation')


class Synonym(BaseModel):
    __tablename__ = 'synonym'

    id: Mapped[int] = mapped_column(primary_key=True,  index=True)
    word_classification_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))
    synonym_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))


class Antonym(BaseModel):
    __tablename__ = 'antonym'
    id: Mapped[int] = mapped_column(primary_key=True,  index=True)
    word_classification_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))
    antonym_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))


class WordClassification(DetailModel):
    __tablename__ = "word_classification"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number_of_times_searched: Mapped[int] = mapped_column(default=1)
    description: Mapped[Union[str, None]]

    examples: Mapped[List['Example']] = relationship(back_populates='word_classification')
    translations: Mapped[List['Translation']] = relationship(back_populates='word_classification')
    source_contents: Mapped[List['SourceContent']] = relationship(back_populates='word_classification')

    word_type_id: Mapped[int] = mapped_column(ForeignKey('word_type.id'))
    word_type: Mapped['WordType'] = relationship(back_populates='word_classifications')

    word_id: Mapped[int] = mapped_column(ForeignKey('word.id'))
    word: Mapped['Word'] = relationship(back_populates='word_classifications')

    # Many to many relationship for synonyms
    synonyms: Mapped[List['WordClassification']] = relationship(
        'WordClassification',
        secondary=Synonym.__tablename__,
        primaryjoin=id == Synonym.word_classification_id,
        secondaryjoin=id == Synonym.synonym_id,
        backref="synonym_of"
    )

    # Many to many relationship for antonyms
    antonyms: Mapped[List['WordClassification']] = relationship(
        'WordClassification',
        secondary=Antonym.__table__,
        primaryjoin=id == Antonym.word_classification_id,
        secondaryjoin=id == Antonym.antonym_id,
        backref="antonym_of"
    )

    @staticmethod
    @db_transaction
    def create(session, data):
        new_register = WordClassification(
            value= data.value,
            description= data.description,
            number_of_times_searched= data.number_of_times_searched,
            word_type_id= data.word_type_id,
            word_id= data.word_id
        )
        session.add(new_register)
        session.commit()
        session.refresh(new_register)

    
    




class Verb(WordClassification):
    __tablename__ = "verb"

    id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'), primary_key=True)

    verbal_tense_id: Mapped[int] = mapped_column(ForeignKey('verbal_tense.id'))
    verbal_tense: Mapped['VerbalTense'] = relationship(back_populates='verbs')

    # Configuración de la relación de herencia
    __mapper_args__ = {
        'inherit_condition': id == WordClassification.id  # Ajusta según tus necesidades específicas
    }
    # Agrega estas líneas para establecer la relación de clave foránea con WordClassification
    #word_classification_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))
    #word_classification: Mapped['WordClassification'] = relationship(back_populates='word_classification')


class VerbalTense(DetailModel):
    __tablename__ = "verbal_tense"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    verbs: Mapped[List['Verb']] = relationship(back_populates='verbal_tense')

    @staticmethod
    @db_transaction
    def create(session, data):
        new_register = VerbalTense(value=data.value)
        session.add(new_register)
        session.commit()
        session.refresh(new_register)


class ApiConnection(BaseModel):
    __tablename__ = "api_connection"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[Union[str, None]]
    description: Mapped[Union[str, None]]

    source_contents: Mapped[List['SourceContent']] = relationship(back_populates='api_connection')


class SourceContent(BaseModel):
    __tablename__ = "source_content"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Union[str, None]]

    word_classification_id: Mapped[Union[int, None]] = mapped_column(ForeignKey('word_classification.id'))
    word_classification: Mapped[Union['WordClassification', None]] = relationship(back_populates='source_contents')

    api_connection_id: Mapped[int] = mapped_column(ForeignKey('api_connection.id'))
    api_connection: Mapped['ApiConnection'] = relationship(back_populates='source_contents')

