from organization.repository import OrganizationAbstractRepository
from organization.models import OrganizationInfo, DocumentCategory

from settings import settings


class OrganizationService:

    def __init__(self, repo: OrganizationAbstractRepository):
        self.repo: OrganizationAbstractRepository = repo

    async def get_all_organization_info(self):
        data = await self.repo.get_all(OrganizationInfo)
        return data

    async def get_all_document_categories(self):
        data = await self.repo.get_all(DocumentCategory)
        return data

    async def get_one_organization_info(self, id: int):
        data = await self.repo.get_one(OrganizationInfo, id)
        if data is None:
            return data
        for document in data.documents:
            document.file = f"{settings.PRODUCTION_URL}{document.file}"
        return data

    async def get_one_document_category(self, id: int):
        data = await self.repo.get_one(DocumentCategory, id)
        if data is None:
            return data
        for document in data.documents:
            document.file = f"{settings.PRODUCTION_URL}{document.file}"
        return data

    async def get_organization(self):
        data = await self.repo.get_organization()
        if data is None:
            return data
        data.logo = f"{settings.PRODUCTION_URL}{data.logo}"
        data.image = f"{settings.PRODUCTION_URL}{data.image}"
        for sport_object in data.sport_objects:
            sport_object.image = f"{settings.PRODUCTION_URL}{sport_object.image}"
        return data
