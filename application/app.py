from pathlib import Path

from litestar import Litestar, Router
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router
from litestar.config.cors import CORSConfig
from litestar.config.allowed_hosts import AllowedHostsConfig

from uvicorn.workers import UvicornWorker

from admin_plugin import AdminPlugin
from database import async_engine
from athletes.admin import AthletesAdmin
from athletes.controller import AthletesController
from coaches.admin import CoachesAdmin
from coaches.controller import CoachesController
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
from upcoming_events.admin import UpcommingEventsAdmin
from upcoming_events.controller import UpcomingEventsController
from vacancies.admin import VacanciesAdmin
from vacancies.controller import VacancyController
from settings import settings


class APIUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "logging.yml",
    }

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
        description='Документация для сайта спортшколы "Тверь"',
        version="0.0.1",
        render_plugins=[ScalarRenderPlugin()],
        path="/documentation",
    ),
    plugins=[admin],
    cors_config=CORSConfig(allow_origins=[settings.CLIENT_URL]),
    allowed_hosts=AllowedHostsConfig(
        allowed_hosts=settings.ALLOWED_HOSTS.split(",")
    ),
    debug=True,
)
