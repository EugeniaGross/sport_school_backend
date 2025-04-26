from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from coaches.models import Coach

CoachDTO = SQLAlchemyDTO[
    Annotated[
        Coach, DTOConfig(exclude={"type_sport_id", "type_sport.description"})
    ]
]
