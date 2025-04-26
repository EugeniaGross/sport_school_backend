from organization.repository import OrganizationMySQLRepository
from organization.service import OrganizationService


async def organization_service():
    return OrganizationService(OrganizationMySQLRepository)
