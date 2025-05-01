from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from organization.models import (
    OrganizationInfo,
    DocumentCategory,
    Organization,
)

OrganizationInfoShortDTO = SQLAlchemyDTO[
    Annotated[
        OrganizationInfo, DTOConfig(exclude={"description", "documents"})
    ]
]

DocumentCategoryShortDTO = SQLAlchemyDTO[
    Annotated[DocumentCategory, DTOConfig(exclude={"documents"})]
]

OrganizationInfoFullDTO = SQLAlchemyDTO[
    Annotated[
        OrganizationInfo,
        DTOConfig(
            exclude={
                "documents.0.id",
                "documents.0.category_id",
                "documents.0.organization_info_id",
                "documents.0.category",
                "documents.0.organization_info",
            }
        ),
    ]
]

DocumentCategoryFullDTO = SQLAlchemyDTO[
    Annotated[
        DocumentCategory,
        DTOConfig(
            exclude={
                "documents.0.id",
                "documents.0.category_id",
                "documents.0.organization_info_id",
                "documents.0.category",
                "documents.0.organization_info",
            }
        ),
    ]
]

OrganizationDTO = SQLAlchemyDTO[
    Annotated[
        Organization,
        DTOConfig(
            exclude={
                "id",
                "phones.0.id",
                "phones.0.organization_id",
                "phones.0.organization",
                "sport_objects.0.organization_id",
                "sport_objects.0.organization",
            }
        ),
    ]
]
