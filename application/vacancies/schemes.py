from typing import Annotated

from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from vacancies.models import Vacancy

VacancyShortDTO = SQLAlchemyDTO[
    Annotated[Vacancy, DTOConfig(exclude={"description", "email", "phone"})]
]

VacancyFullDTO = SQLAlchemyDTO[Vacancy]
