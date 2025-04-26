from types_sports.repository import TypeSportMySQLRepository
from types_sports.service import TypeSportsService


async def types_sports_service():
    return TypeSportsService(TypeSportMySQLRepository)
