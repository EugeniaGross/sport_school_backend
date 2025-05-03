from typing import Optional

from upcoming_events.repository import UpcomingEventsAbstractRepository

from settings import settings


class UpcomingEventsService:

    def __init__(self, repo: UpcomingEventsAbstractRepository):
        self.repo: UpcomingEventsAbstractRepository = repo

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
        if data:
            data.image = f"{settings.PRODUCTION_URL}{data.image}"
        return data

    async def get_total_count(self, type_sport: Optional[str]):
        if type_sport:
            return await self.repo.get_total_count_with_filter(type_sport)
        return await self.repo.get_total_count()
