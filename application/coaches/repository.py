from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from coaches.models import Coach
from database import async_session


class CoachesAbstractRepository(ABC):

    @abstractmethod
    async def get_with_filter():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError


class CoachesMySQLRepository(CoachesAbstractRepository):

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(Coach).options(joinedload(Coach.type_sport))
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_with_filter(type_sports):
        async with async_session() as session:
            query = (
                select(Coach)
                .filter(Coach.type_sport.has(name=type_sports))
                .options(joinedload(Coach.type_sport))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(
                Coach, id, options=[joinedload(Coach.type_sport)]
            )
            return result
