from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from upcoming_events.models import UpcommingEvents

UpcommingEventsShortDTO = SQLAlchemyDTO[
    Annotated[
        UpcommingEvents,
        DTOConfig(exclude={"description", "type_sport_id", "type_sport.description"}),
    ]
]

UpcommingEventsFullDTO = SQLAlchemyDTO[
    Annotated[
        UpcommingEvents,
        DTOConfig(exclude={"type_sport_id", "type_sport.description"}),
    ]
]
