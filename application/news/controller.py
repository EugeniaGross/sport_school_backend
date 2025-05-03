from typing import Optional

from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.pagination import OffsetPagination

from news.dependiences import news_service
from news.models import News
from news.pagination import NewsOffsetPaginator
from news.schemes import (
    NewsFullDTO,
    NewsShortDTO,
)
from news.service import NewsService


class NewsController(Controller):
    path = "/news"
    dependencies = {"news_service": Provide(news_service)}

    @get(
        "/",
        return_dto=NewsShortDTO,
        dependencies={"paginator": Provide(NewsOffsetPaginator)},
    )
    async def get_with_filter_news(
        self,
        news_service: NewsService,
        paginator: NewsOffsetPaginator,
        limit: int,
        offset: int,
        type_sport: Optional[str] = None,
    ) -> OffsetPagination[News]:
        return await paginator(limit=limit, offset=offset)

    @get("/{news_id:int}", return_dto=NewsFullDTO)
    async def get_one_news(
        self,
        news_id: int,
        news_service: NewsService,
    ) -> News:
        data = await news_service.get_one(news_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
