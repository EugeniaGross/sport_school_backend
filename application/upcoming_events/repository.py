from abc import ABC, abstractmethod

from sqlalchemy import select, func, desc
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

    @abstractmethod
    async def get_total_count():
        raise NotImplementedError

    @abstractmethod
    async def get_total_count_with_filter():
        raise NotImplementedError


class UpcomingEventsMySQLRepository(UpcomingEventsAbstractRepository):

    @staticmethod
    async def get_all(limit: int, offset: int):
        async with async_session() as session:
            query = (
                select(UpcommingEvents)
                .options(joinedload(UpcommingEvents.type_sport))
                .offset(offset)
                .limit(limit)
                .order_by(desc(UpcommingEvents.date))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_with_filter(type_sports: str, limit: int, offset: int):
        async with async_session() as session:
            query = (
                select(UpcommingEvents)
                .filter(UpcommingEvents.type_sport.has(name=type_sports))
                .options(joinedload(UpcommingEvents.type_sport))
                .offset(offset)
                .limit(limit)
                .order_by(desc(UpcommingEvents.date))
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

    @staticmethod
    async def get_total_count():
        async with async_session() as session:
            count = await session.scalar(select(func.count(UpcommingEvents.id)))
            return count

    @staticmethod
    async def get_total_count_with_filter(type_sports):
        async with async_session() as session:
            count = await session.scalar(
                select(func.count(UpcommingEvents.id)).filter(
                    UpcommingEvents.type_sport.has(name=type_sports)
                )
            )
            return count
