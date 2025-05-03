from typing import Optional

from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.connection import Request

from athletes.dependiences import athletes_service
from athletes.models import Athlet
from athletes.schemes import AthletDTO
from athletes.service import AthletService


class AthletesController(Controller):
    path = "/athletes"
    dependencies = {"athletes_service": Provide(athletes_service)}

    @get("/", return_dto=AthletDTO)
    async def get_with_filter_athletes(
        self,
        athletes_service: AthletService,
        type_sport: Optional[str] = None,
    ) -> list[Athlet]:
        data = await athletes_service.get_with_filter(type_sport)
        return data

    @get("/{athlet_id:int}", return_dto=AthletDTO)
    async def get_one_athlet(
        self, athlet_id: int, athletes_service: AthletService
    ) -> Athlet:
        data = await athletes_service.get_one(athlet_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
