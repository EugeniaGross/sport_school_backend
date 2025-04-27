from typing import Optional


from litestar.connection import Request
from news.repository import NewsAbstractRepository


class NewsService:

    def __init__(self, repo: NewsAbstractRepository):
        self.repo: NewsAbstractRepository = repo

    async def get_with_filter(
        self,
        request: Request,
        type_sport: Optional[str],
        offset: int,
        limit: int,
    ):
        if type_sport is None:
            data = await self.repo.get_all(limit, offset)
        else:
            data = await self.repo.get_with_filter(type_sport, limit, offset)
        for element in data:
            element.image = f"{request.base_url}statics/images/{element.image}"
        return data

    async def get_one(self, request: Request, id: int):
        data = await self.repo.get_one(id)
        if data is None:
            return data
        data.image = f"{request.base_url}statics/images/{data.image}"
        for photo in data.photos:
            photo.image = f"{request.base_url}statics/images/{photo.image}"
        return data

    async def get_total_count(self, type_sport: Optional[str]):
        if type_sport:
            return await self.repo.get_total_count_with_filter(type_sport)
        return await self.repo.get_total_count()
