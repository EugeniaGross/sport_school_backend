from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from types_sports.models import TypesSports

TypeSportShortDTO = SQLAlchemyDTO[
    Annotated[TypesSports, DTOConfig(exclude={"description"})]
]

TypeSportFullDTO = SQLAlchemyDTO[TypesSports]
