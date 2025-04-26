from typing import Optional

from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.connection import Request

from coaches.dependiences import coaches_service
from coaches.models import Coach
from coaches.schemes import CoachDTO
from coaches.service import CoachService


class CoachesController(Controller):
    path = "/coaches"
    dependencies = {"coaches_service": Provide(coaches_service)}

    @get("/", return_dto=CoachDTO)
    async def get_with_filter_coaches(
        self,
        request: Request,
        coaches_service: CoachService,
        type_sport: Optional[str] = None,
    ) -> list[Coach]:
        data = await coaches_service.get_with_filter(request, type_sport)
        return data

    @get("/{coach_id:int}", return_dto=CoachDTO)
    async def get_one_coach(
        self, request: Request, coach_id: int, coaches_service: CoachService
    ) -> Coach:
        data = await coaches_service.get_one(request, coach_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
