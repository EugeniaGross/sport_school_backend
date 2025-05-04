from typing import Optional, cast

from litestar.pagination import AbstractAsyncOffsetPaginator

from upcoming_events.models import UpcommingEvents
from upcoming_events.service import UpcomingEventsService


class UpcommingEventsOffsetPaginator(AbstractAsyncOffsetPaginator[UpcommingEvents]):
    def __init__(
        self,
        type_sport: Optional[str],
        upcoming_events_service: UpcomingEventsService,
    ) -> None:
        self.upcoming_events_service = upcoming_events_service
        self.type_sport = type_sport

    async def get_total(self) -> int:
        return cast(
            "int",
            await self.upcoming_events_service.get_total_count(self.type_sport),
        )

    async def get_items(self, limit: int, offset: int) -> list[UpcommingEvents]:
        return await self.upcoming_events_service.get_with_filter(
            self.type_sport, offset, limit
        )
