from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from athletes.models import Athlet

AthletDTO = SQLAlchemyDTO[
    Annotated[Athlet, DTOConfig(exclude={"type_sport_id", "type_sport.description"})]
]
