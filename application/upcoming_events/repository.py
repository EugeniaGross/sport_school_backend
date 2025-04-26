from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from upcoming_events.models import UpcommingEvents
from database import async_session


class UpcomingEventsAbstractRepository(ABC):

    @abstractmethod
    async def get_with_filter():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError


class UpcomingEventsMySQLRepository(UpcomingEventsAbstractRepository):

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(UpcommingEvents).options(
                joinedload(UpcommingEvents.type_sport)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_with_filter(type_sports):
        async with async_session() as session:
            query = (
                select(UpcommingEvents)
                .filter(UpcommingEvents.type_sport.has(name=type_sports))
                .options(joinedload(UpcommingEvents.type_sport))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(
                UpcommingEvents,
                id,
                options=[joinedload(UpcommingEvents.type_sport)],
            )
            return result
