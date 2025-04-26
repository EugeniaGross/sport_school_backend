from coaches.repository import CoachesMySQLRepository
from coaches.service import CoachService


async def coaches_service():
    return CoachService(CoachesMySQLRepository)
