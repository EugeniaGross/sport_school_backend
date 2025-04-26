from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException

from vacancies.dependiences import vacancies_service
from vacancies.models import Vacancy
from vacancies.schemes import VacancyShortDTO, VacancyFullDTO
from vacancies.service import VacancyService


class VacancyController(Controller):
    path = "/vacancies"
    dependencies = {"vacancies_service": Provide(vacancies_service)}

    @get("/", return_dto=VacancyShortDTO)
    async def get_all_vacancies(
        self, vacancies_service: VacancyService
    ) -> list[Vacancy]:
        data = await vacancies_service.get_all()
        return data

    @get("/{vacancy_id:int}", return_dto=VacancyFullDTO)
    async def get_one_vacancy(
        self, vacancy_id: int, vacancies_service: VacancyService
    ) -> Vacancy:
        data = await vacancies_service.get_one(vacancy_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
