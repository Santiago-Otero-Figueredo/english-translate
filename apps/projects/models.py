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

