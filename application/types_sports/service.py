from types_sports.repository import TypeSportAbstractRepository

from settings import settings


class TypeSportsService:

    def __init__(self, repo: TypeSportAbstractRepository):
        self.repo: TypeSportAbstractRepository = repo

    async def get_all(self):
        data = await self.repo.get_all()
        return data

    async def get_one(self, id):
        data = await self.repo.get_one(id)
        for coach in data.coaches:
            coach.image = f"{settings.PRODUCTION_URL}{coach.image}"
        for athlet in data.athletes:
            athlet.image = f"{settings.PRODUCTION_URL}{athlet.image}"
        for news in data.news:
            news.image = f"{settings.PRODUCTION_URL}{news.image}"
        for uncoming_event in data.uncoming_events:
            uncoming_event.image = (
                f"{settings.PRODUCTION_URL}{uncoming_event.image}"
            )
        return data
