from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from organization.models import (
    OrganizationInfo,
    DocumentCategory,
    Organization,
)
from database import async_session


class OrganizationAbstractRepository(ABC):

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_organization():
        raise NotImplementedError


class OrganizationMySQLRepository(OrganizationAbstractRepository):

    @staticmethod
    async def get_all(model: Union[OrganizationInfo, DocumentCategory]):
        async with async_session() as session:
            query = select(model)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_one(
        model: Union[OrganizationInfo, DocumentCategory], id: int
    ):
        async with async_session() as session:
            result = await session.get(
                model, id, options=[joinedload(model.documents)]
            )
            return result

    @staticmethod
    async def get_organization():
        async with async_session() as session:
            query = (
                select(Organization)
                .options(joinedload(Organization.phones))
                .options(joinedload(Organization.sport_objects))
            )
            result = await session.execute(query)
            return result.unique().scalars().one_or_none()
