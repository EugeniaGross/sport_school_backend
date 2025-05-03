from athletes.repository import AthletesAbstractRepository

from settings import settings


class AthletService:

    def __init__(self, repo: AthletesAbstractRepository):
        self.repo: AthletesAbstractRepository = repo

    async def get_with_filter(self, type_sport: str):
        if type_sport is None:
            data = await self.repo.get_all()
        else:
            data = await self.repo.get_with_filter(type_sport)
        for element in data:
            element.image = f"{settings.PRODUCTION_URL}{element.image}"
        return data

    async def get_one(self, id: int):
        data = await self.repo.get_one(id)
        if data:
            data.image = f"{settings.PRODUCTION_URL}{data.image}"
        return data
