from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from news.models import News

NewsShortDTO = SQLAlchemyDTO[
    Annotated[
        News,
        DTOConfig(
            exclude={
                "description",
                "photos",
                "type_sport_id",
                "type_sport.description",
            }
        ),
    ]
]

NewsFullDTO = SQLAlchemyDTO[
    Annotated[
        News,
        DTOConfig(
            exclude={
                "type_sport_id",
                "type_sport.description",
                "photos.0.id",
                "photos.0.news_id",
                "photos.0.news",
            }
        ),
    ]
]
