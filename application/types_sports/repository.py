from abc import ABC, abstractmethod

from sqlalchemy import select

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
            query = select(TypesSports)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(TypesSports, id)
            return result
