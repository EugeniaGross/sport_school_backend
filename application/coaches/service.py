from litestar.connection import Request
from coaches.repository import CoachesAbstractRepository


class CoachService:

    def __init__(self, repo: CoachesAbstractRepository):
        self.repo: CoachesAbstractRepository = repo

    async def get_with_filter(self, request: Request, type_sport: str):
        if type_sport is None:
            data = await self.repo.get_all()
        else:
            data = await self.repo.get_with_filter(type_sport)
        for element in data:
            element.image = f"{request.base_url}statics/images/{element.image}"
        return data

    async def get_one(self, request: Request, id: int):
        data = await self.repo.get_one(id)
        if data:
            data.image = f"{request.base_url}statics/images/{data.image}"
        return data
