from types_sports.repository import TypeSportAbstractRepository


class TypeSportsService:

    def __init__(self, repo: TypeSportAbstractRepository):
        self.repo: TypeSportAbstractRepository = repo

    async def get_all(self):
        data = await self.repo.get_all()
        return data

    async def get_one(self, id):
        data = await self.repo.get_one(id)
        return data
