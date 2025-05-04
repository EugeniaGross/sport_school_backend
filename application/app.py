from pathlib import Path

from litestar import Litestar, Router, post, Response
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router
from litestar.config.cors import CORSConfig
from litestar.config.allowed_hosts import AllowedHostsConfig
from uvicorn.workers import UvicornWorker

from admin_plugin import AdminPlugin, AdminAuth
from database import async_engine
from athletes.admin import AthletesAdmin
from athletes.controller import AthletesController
from coaches.admin import CoachesAdmin
from coaches.controller import CoachesController
from commands import CLIPlugin
from news.admin import NewsAdmin, PhotoNewsAdmin
from news.controller import NewsController
from organization.admin import (
    OrganizationDocumentsAdmin,
    OrganizationInfoAdmin,
    DocumentCategoryAdmin,
    OrganizationAdmin,
    OrganizationPhoneAdmin,
    OrganizationSportObjectAdmin,
)
from organization.controllers import OrganizationController
from types_sports.admin import TypesSportsAdmin
from types_sports.controller import TypesSportsController
from schemes import EmailBody
from upcoming_events.admin import UpcommingEventsAdmin
from upcoming_events.controller import UpcomingEventsController
from utils.email import send_email
from vacancies.admin import VacanciesAdmin
from vacancies.controller import VacancyController
from settings import settings, logging_config, logger


class APIUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "logging.yml",
    }


@post("/send_to_email", status_code=200)
async def send_to_email(data: EmailBody) -> None:
    try:
        await send_email(data.name, data.phone, data.message, data.email)
    except Exception as e:
        logger.error(e)
        return Response(
            content={"detail": "Не удалось отправить сообщение"},
            status_code=500,
        )


api_v1_router = Router(
    path="/api/v1",
    route_handlers=[
        OrganizationController,
        TypesSportsController,
        CoachesController,
        AthletesController,
        UpcomingEventsController,
        NewsController,
        VacancyController,
        send_to_email,
    ],
)

admin = AdminPlugin(
    views=[
        OrganizationAdmin,
        OrganizationPhoneAdmin,
        OrganizationInfoAdmin,
        DocumentCategoryAdmin,
        OrganizationDocumentsAdmin,
        OrganizationSportObjectAdmin,
        TypesSportsAdmin,
        CoachesAdmin,
        AthletesAdmin,
        UpcommingEventsAdmin,
        NewsAdmin,
        PhotoNewsAdmin,
        VacanciesAdmin,
    ],
    engine=async_engine,
    title="Панель администратора",
    authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
)

app = Litestar(
    route_handlers=[
        create_static_files_router(path="/statics", directories=["statics"]),
        api_v1_router,
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    openapi_config=OpenAPIConfig(
        title="Sport School API",
        description='Документация API для сайта спортшколы "Тверь"',
        version="0.0.1",
        render_plugins=[ScalarRenderPlugin()],
        path="/documentation",
    ),
    plugins=[admin, CLIPlugin()],
    cors_config=CORSConfig(allow_origins=[settings.CLIENT_URL]),
    allowed_hosts=AllowedHostsConfig(allowed_hosts=settings.ALLOWED_HOSTS.split(",")),
    logging_config=logging_config,
)
