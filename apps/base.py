from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from typing import Union
from datetime import datetime

from core.database import Base
# Definición de las tablas


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)


    @property
    def created_at_formatted(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')

    @classmethod
    async def get_by_id(cls, id_search: int, session):
        return session.query(cls).filter(cls.id == id_search).first()

    @classmethod
    async def get_all(cls, session):
        return session.query(cls).order_by(cls.created_at).all()

    @classmethod
    async def get_by_filter(cls, filters: dict, session, order_by:dict = {}):
        query = session.query(cls)

        if filters:
            query = query.filter_by(**filters)

        if order_by:
            order_clauses = [
                getattr(cls, column).desc() if order == 'desc' else getattr(cls, column)
                for column, order in order_by.items()
            ]
            query = query.order_by(*order_clauses)
        else:
            query = query.order_by(cls.created_at)

        return query.all()

    @classmethod
    async def get_all_active(cls, session):
        return session.query(cls).filter(cls.is_active == True).all()


class DetailModel(BaseModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String(50))
    #description: Mapped[Union[str, None]]


    @classmethod
    async def get_by_value(cls, name: str, session):
        return session.query(cls).filter(cls.name == name).first()



