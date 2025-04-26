from abc import ABC, abstractmethod

from sqlalchemy import select

from vacancies.models import Vacancy
from database import async_session


class VacancyAbstractRepository(ABC):

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError


class VacancyMySQLRepository(VacancyAbstractRepository):

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = select(Vacancy)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(Vacancy, id)
            return result
