from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.connection import Request

from types_sports.dependiences import types_sports_service
from types_sports.models import TypesSports
from types_sports.schemes import TypeSportShortDTO, TypeSportFullDTO
from types_sports.service import TypeSportsService


class TypesSportsController(Controller):
    path = "/types_sports"
    dependencies = {"types_sports_service": Provide(types_sports_service)}

    @get("/", return_dto=TypeSportShortDTO)
    async def get_all_types_sports(
        self, types_sports_service: TypeSportsService
    ) -> list[TypesSports]:
        data = await types_sports_service.get_all()
        return data

    @get("/{type_sport_id:int}", return_dto=TypeSportFullDTO)
    async def get_one_type_sport(
        self, type_sport_id: int, types_sports_service: TypeSportsService
    ) -> TypesSports:
        data = await types_sports_service.get_one(type_sport_id)
        if data is None:
            raise NotFoundException("Not found")
        return data
