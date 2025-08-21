from typing import Optional

from news.repository import NewsAbstractRepository

from settings import settings


class NewsService:

    def __init__(self, repo: NewsAbstractRepository):
        self.repo: NewsAbstractRepository = repo

    async def get_with_filter(
        self,
        type_sport: Optional[str],
        offset: int,
        limit: int,
    ):
        if type_sport is None:
            data = await self.repo.get_all(limit, offset)
        else:
            data = await self.repo.get_with_filter(type_sport, limit, offset)
        for element in data:
            element.image = f"{settings.PRODUCTION_URL}{element.image}"
        return data

    async def get_one(self, id: int):
        data = await self.repo.get_one(id)
        if data is None:
            return data
        data.image = f"{settings.PRODUCTION_URL}{data.image}"
        for photo in data.photos:
            photo.image = f"{settings.PRODUCTION_URL}{photo.image}"
        data.photos = sorted(data.photos, key=lambda x: x.order)
        return data

    async def get_total_count(self, type_sport: Optional[str]):
        if type_sport:
            return await self.repo.get_total_count_with_filter(type_sport)
        return await self.repo.get_total_count()
