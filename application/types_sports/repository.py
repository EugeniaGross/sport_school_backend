from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from types_sports.models import TypesSports
from database import async_session


class TypeSportAbstractRepository(ABC):

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError


class TypeSportMySQLRepository(TypeSportAbstractRepository):

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(TypesSports).options(
                joinedload(TypesSports.uncoming_events),
                joinedload(TypesSports.coaches),
                joinedload(TypesSports.athletes),
                joinedload(TypesSports.news),
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            query = select(TypesSports).where(TypesSports.id == id).options(
                joinedload(TypesSports.uncoming_events),
                joinedload(TypesSports.coaches),
                joinedload(TypesSports.athletes),
                joinedload(TypesSports.news),
            )
            result = await session.execute(query)
            return result.unique().scalars().first()
