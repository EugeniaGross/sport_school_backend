from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from athletes.models import Athlet
from database import async_session


class AthletesAbstractRepository(ABC):

    @abstractmethod
    async def get_with_filter():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError


class AthletesMySQLRepository(AthletesAbstractRepository):

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(Athlet).options(joinedload(Athlet.type_sport))
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_with_filter(type_sports):
        async with async_session() as session:
            query = (
                select(Athlet)
                .filter(Athlet.type_sport.has(name=type_sports))
                .options(joinedload(Athlet.type_sport))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(
                Athlet, id, options=[joinedload(Athlet.type_sport)]
            )
            return result
