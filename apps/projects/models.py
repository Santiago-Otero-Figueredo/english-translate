from sqlalchemy import CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import get_session

from typing import TYPE_CHECKING, List, Union

from datetime import datetime

from ..base import DetailModel


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


class WordType(DetailModel):
    __tablename__ = "word_type"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_classifications: Mapped[List['WordClassification']] = relationship(back_populates='word_type')


class Word(DetailModel):
    __tablename__ = "word"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_classifications: Mapped[List['WordClassification']] = relationship(back_populates='word')


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
    level: Mapped[int] = mapped_column(default=0)
    description: Mapped[Union[str, None]]
    source_content: Mapped[Union[str, None]] = mapped_column(String(150), default='')

    examples: Mapped[List['Example']] = relationship(back_populates='word_classification')
    translations: Mapped[List['Translation']] = relationship(back_populates='word_classification')


    word_type_id: Mapped[int] = mapped_column(ForeignKey('word_type.id'))
    word_type: Mapped['WordType'] = relationship(back_populates='words_classification')

    word_id: Mapped[int] = mapped_column(ForeignKey('word.id'))
    word: Mapped['Word'] = relationship(back_populates='words_classification')


class Verb(WordClassification):
    __tablename__ = "verb"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    verbal_tense_id: Mapped[int] = mapped_column(ForeignKey('verbal_tense.id'))
    verbal_tense: Mapped['VerbalTense'] = relationship(back_populates='verbs')

    # Agrega estas líneas para establecer la relación de clave foránea con WordClassification
    word_classification_id: Mapped[int] = mapped_column(ForeignKey('word_classification.id'))
    word_classification: Mapped['WordClassification'] = relationship(back_populates='__class__')

class VerbalTense(DetailModel):
    __tablename__ = "verbal_tense"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    verbs: Mapped[List['Verb']] = relationship(back_populates='verbal_tense')






