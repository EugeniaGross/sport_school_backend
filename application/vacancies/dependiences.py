from vacancies.repository import VacancyMySQLRepository
from vacancies.service import VacancyService


async def vacancies_service():
    return VacancyService(VacancyMySQLRepository)
