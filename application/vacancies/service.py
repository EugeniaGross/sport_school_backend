from vacancies.repository import VacancyAbstractRepository


class VacancyService:

    def __init__(self, repo: VacancyAbstractRepository):
        self.repo: VacancyAbstractRepository = repo

    async def get_all(self):
        data = await self.repo.get_all()
        return data

    async def get_one(self, id):
        data = await self.repo.get_one(id)
        return data
