from abc import ABC, abstractmethod

from sqlalchemy import select, func, desc
from sqlalchemy.orm import joinedload

from news.models import News
from database import async_session


class NewsAbstractRepository(ABC):

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


class NewsMySQLRepository(NewsAbstractRepository):

    @staticmethod
    async def get_all(limit: int, offset: int):
        async with async_session() as session:
            query = (
                select(News)
                .options(joinedload(News.type_sport))
                .offset(offset)
                .limit(limit)
                .order_by(desc(News.date))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_with_filter(type_sports: str, limit: int, offset: int):
        async with async_session() as session:
            query = (
                select(News)
                .filter(News.type_sport.has(name=type_sports))
                .options(joinedload(News.type_sport))
                .order_by(desc(News.date))
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(
                News,
                id,
                options=[joinedload(News.type_sport), joinedload(News.photos)],
            )
            return result

    @staticmethod
    async def get_total_count():
        async with async_session() as session:
            count = await session.scalar(select(func.count(News.id)))
            return count

    @staticmethod
    async def get_total_count_with_filter(type_sports):
        async with async_session() as session:
            count = await session.scalar(
                select(func.count(News.id)).filter(
                    News.type_sport.has(name=type_sports)
                )
            )
            return count
