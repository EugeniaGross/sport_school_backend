from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from users.models import Users
from database import async_session


class UsersAbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_email():
        raise NotImplementedError


class UsersMySQLRepository(UsersAbstractRepository):

    @staticmethod
    async def add_one(data: dict):
        async with async_session() as session:
            query = insert(Users).values(**data)
            result = await session.execute(query)
            await session.commit()
            return result.inserted_primary_key

    @staticmethod
    async def get_one(id: int):
        async with async_session() as session:
            result = await session.get(Users, id)
            return result

    @staticmethod
    async def get_one_by_email(email: str):
        async with async_session() as session:
            query = select(Users).where(Users.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
