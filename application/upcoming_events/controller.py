from typing import Optional

from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.connection import Request
from litestar.pagination import OffsetPagination

from upcoming_events.dependiences import upcoming_events_service
from upcoming_events.models import UpcommingEvents
from upcoming_events.schemes import (
    UpcommingEventsFullDTO,
    UpcommingEventsShortDTO,
)
from upcoming_events.pagination import UpcommingEventsOffsetPaginator
from upcoming_events.service import UpcomingEventsService


class UpcomingEventsController(Controller):
    path = "/upcomming_events"
    dependencies = {
        "upcoming_events_service": Provide(upcoming_events_service)
    }

    @get(
        "/",
        return_dto=UpcommingEventsShortDTO,
        dependencies={"paginator": Provide(UpcommingEventsOffsetPaginator)},
    )
    async def get_with_filter_upcoming_events(
        self,
        upcoming_events_service: UpcomingEventsService,
        paginator: UpcommingEventsOffsetPaginator,
        limit: int,
        offset: int,
        type_sport: Optional[str] = None,
    ) -> OffsetPagination[UpcommingEvents]:
        return await paginator(limit=limit, offset=offset)

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
