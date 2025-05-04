from typing import Optional, cast

from litestar.pagination import AbstractAsyncOffsetPaginator

from news.models import News
from news.service import NewsService


class NewsOffsetPaginator(AbstractAsyncOffsetPaginator[News]):
    def __init__(
        self,
        type_sport: Optional[str],
        news_service: NewsService,
    ) -> None:
        self.news_service = news_service
        self.type_sport = type_sport

    async def get_total(self) -> int:
        return cast("int", await self.news_service.get_total_count(self.type_sport))

    async def get_items(self, limit: int, offset: int) -> list[News]:
        return await self.news_service.get_with_filter(self.type_sport, offset, limit)
