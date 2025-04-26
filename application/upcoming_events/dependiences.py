from upcoming_events.repository import UpcomingEventsMySQLRepository
from upcoming_events.service import UpcomingEventsService


async def upcoming_events_service():
    return UpcomingEventsService(UpcomingEventsMySQLRepository)
