from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException

from organization.dependiences import organization_service
from organization.models import (
    OrganizationInfo,
    DocumentCategory,
    Organization,
)
from organization.schemes import (
    DocumentCategoryFullDTO,
    DocumentCategoryShortDTO,
    OrganizationInfoFullDTO,
    OrganizationInfoShortDTO,
    OrganizationDTO,
)
from organization.service import OrganizationService


class OrganizationController(Controller):
    path = "/organization"
    dependencies = {"organization_service": Provide(organization_service)}

    @get("/", return_dto=OrganizationDTO)
    async def get_organization(
        self,
        organization_service: OrganizationService,
    ) -> Organization:
        data = await organization_service.get_organization()
        if data is None:
            raise NotFoundException("Not found")
        return data

    @get("/document_categoties", return_dto=DocumentCategoryShortDTO)
    async def get_all_document_categories(
        self,
        organization_service: OrganizationService,
    ) -> list[DocumentCategory]:
        data = await organization_service.get_all_document_categories()
        return data

    @get(
        "/document_categoties/{document_category_id:int}",
        return_dto=DocumentCategoryFullDTO,
    )
    async def get_one_document_category(
        self,
        document_category_id: int,
        organization_service: OrganizationService,
    ) -> DocumentCategory:
        data = await organization_service.get_one_document_category(
            document_category_id
        )
        if data is None:
            raise NotFoundException("Not found")
        return data

    @get("/information", return_dto=OrganizationInfoShortDTO)
    async def get_all_organization_info(
        self,
        organization_service: OrganizationService,
    ) -> list[OrganizationInfo]:
        data = await organization_service.get_all_organization_info()
        return data

    @get("/information/{information_id:int}", return_dto=OrganizationInfoFullDTO)
    async def get_one_organization_info(
        self,
        information_id: int,
        organization_service: OrganizationService,
    ) -> OrganizationInfo:
        data = await organization_service.get_one_organization_info(information_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
