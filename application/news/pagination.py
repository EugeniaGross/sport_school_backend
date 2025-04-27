from typing import Optional, cast

from litestar.connection import Request
from litestar.pagination import AbstractAsyncOffsetPaginator

from news.models import News
from news.service import NewsService


class NewsOffsetPaginator(AbstractAsyncOffsetPaginator[News]):
    def __init__(
        self,
        request: Request,
        type_sport: Optional[str],
        news_service: NewsService,
    ) -> None:
        self.news_service = news_service
        self.request = request
        self.type_sport = type_sport

    async def get_total(self) -> int:
        return cast(
            "int", await self.news_service.get_total_count(self.type_sport)
        )

    async def get_items(self, limit: int, offset: int) -> list[News]:
        return await self.news_service.get_with_filter(
            self.request, self.type_sport, offset, limit
        )
