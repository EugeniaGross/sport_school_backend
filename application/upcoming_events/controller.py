from typing import Optional

from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.connection import Request

from upcoming_events.dependiences import upcoming_events_service
from upcoming_events.models import UpcommingEvents
from upcoming_events.schemes import (
    UpcommingEventsFullDTO,
    UpcommingEventsShortDTO,
)
from upcoming_events.service import UpcomingEventsService


class UpcomingEventsController(Controller):
    path = "/upcomming_events"
    dependencies = {
        "upcoming_events_service": Provide(upcoming_events_service)
    }

    @get("/", return_dto=UpcommingEventsShortDTO)
    async def get_with_filter_upcoming_events(
        self,
        request: Request,
        upcoming_events_service: UpcomingEventsService,
        type_sport: Optional[str] = None,
    ) -> list[UpcommingEvents]:
        data = await upcoming_events_service.get_with_filter(
            request, type_sport
        )
        return data

    @get("/{upcoming_event_id:int}", return_dto=UpcommingEventsFullDTO)
    async def get_one_upcoming_event(
        self,
        request: Request,
        upcoming_event_id: int,
        upcoming_events_service: UpcomingEventsService,
    ) -> UpcommingEvents:
        data = await upcoming_events_service.get_one(
            request, upcoming_event_id
        )
        if data is None:
            raise NotFoundException("Not found")
        return data
