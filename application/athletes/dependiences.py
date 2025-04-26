from athletes.repository import AthletesMySQLRepository
from athletes.service import AthletService


async def athletes_service():
    return AthletService(AthletesMySQLRepository)
