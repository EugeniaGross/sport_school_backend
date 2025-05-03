from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from types_sports.models import TypesSports

TypeSportShortDTO = SQLAlchemyDTO[
    Annotated[
        TypesSports,
        DTOConfig(
            exclude={
                "description",
                "coaches",
                "athletes",
                "uncoming_events",
                "news",
            }
        ),
    ]
]

TypeSportFullDTO = SQLAlchemyDTO[
    Annotated[
        TypesSports,
        DTOConfig(
            exclude={
                "coaches.0.description",
                "coaches.0.type_sport",
                "coaches.0.type_sport_id",
                "athletes.0.type_sport",
                "athletes.0.type_sport_id",
                "uncoming_events.0.description",
                "uncoming_events.0.type_sport",
                "uncoming_events.0.type_sport_id",
                "news.0.description",
                "news.0.type_sport_id",
                "news.0.type_sport",
                "news.0.photos",
            }
        ),
    ]
]
