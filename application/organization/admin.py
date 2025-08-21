from sqladmin import ModelView
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import select
from sqladmin.pagination import Pagination
from starlette.requests import Request
from wtforms import TextAreaField
from organization.models import (
    Organization,
    OrganizationPhone,
    OrganizationSportObject,
    OrganizationDocument,
    OrganizationInfo,
    DocumentCategory,
)

from admin_plugin import FileField
from settings import settings


class OrganizationAdmin(ModelView, model=Organization):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "организацию"
    name_plural = "Организация"
    column_list = [
        Organization.name,
    ]
    column_labels = {
        Organization.logo: "Логотип",
        Organization.name: "Название организации",
        Organization.image: "Постер",
        Organization.email: "Электронная почта",
        Organization.address: "Адрес",
        Organization.monday_hours: "Режим работы в понедельник",
        Organization.tuesday_hours: "Режим работы во вторник",
        Organization.wednesday_hours: "Режим работы в среду",
        Organization.thursday_hours: "Режим работы в четверг",
        Organization.friday_hours: "Режим работы в пятницу",
        Organization.saturday_hours: "Режим работы в субботу",
        Organization.sunday_hours: "Режим работы в воскресение",
        Organization.phones: "Номера телефонов",
        Organization.telegram_link: "Телеграм",
        Organization.vk_link: "В контакте",
        Organization.whats_app_link: "WhatsApp",
        Organization.rutube_link: "Rutube",
        Organization.sport_objects: "Спортивные объекты",
    }
    column_details_list = [Organization.name]
    form_overrides = dict(image=FileField, logo=FileField)
    page_size = 50
    can_delete = False


class OrganizationPhoneAdmin(ModelView, model=OrganizationPhone):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "телефон"
    name_plural = "Телефоны организации"
    column_list = [OrganizationPhone.phone, OrganizationPhone.division]
    column_labels = {
        OrganizationPhone.organization: "Организация",
        OrganizationPhone.division: "Подразделение",
        OrganizationPhone.phone: "Номер телефона",
    }
    column_details_list = [OrganizationPhone.phone]
    page_size = 50


class OrganizationSportObjectAdmin(ModelView, model=OrganizationSportObject):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "спортивный объект"
    name_plural = "Спортивные объекты"
    column_list = [
        OrganizationSportObject.name,
        OrganizationSportObject.address,
    ]
    column_labels = {
        OrganizationSportObject.name: "Название",
        OrganizationSportObject.image: "Постер",
        OrganizationSportObject.email: "Электронная почта",
        OrganizationSportObject.address: "Адрес",
        OrganizationSportObject.phone: "Номера телефона",
        OrganizationSportObject.url: "URL адрес",
        OrganizationSportObject.description: "Описание",
        Organization.monday_hours: "Режим работы в понедельник",
        Organization.tuesday_hours: "Режим работы во вторник",
        Organization.wednesday_hours: "Режим работы в среду",
        Organization.thursday_hours: "Режим работы в четверг",
        Organization.friday_hours: "Режим работы в пятницу",
        Organization.saturday_hours: "Режим работы в субботу",
        Organization.sunday_hours: "Режим работы в воскресение",
        OrganizationSportObject.organization: "Организация",
        OrganizationSportObject.latitude: "Широта",
        OrganizationSportObject.longitude: "Долгота",
    }
    column_details_list = [
        OrganizationSportObject.name,
        OrganizationSportObject.address,
    ]
    column_searchable_list = [OrganizationSportObject.name]
    form_overrides = dict(description=TextAreaField, image=FileField)
    page_size = 50


class OrganizationInfoAdmin(ModelView, model=OrganizationInfo):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "информацию"
    name_plural = "Сведения об организации"
    column_list = [
        OrganizationInfo.category,
    ]
    column_labels = {
        OrganizationInfo.category: "Категория",
        OrganizationInfo.description: "Описание",
        OrganizationInfo.documents: "Документы",
        OrganizationInfo.order: "Порядок отображения",
    }
    column_searchable_list = [OrganizationInfo.category]
    column_details_list = [OrganizationInfo.category]
    form_overrides = dict(description=TextAreaField)
    page_size = 50


class DocumentCategoryAdmin(ModelView, model=DocumentCategory):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "категорию"
    name_plural = "Категории документов"
    column_list = [
        DocumentCategory.name,
    ]
    column_labels = {
        DocumentCategory.name: "Название",
        DocumentCategory.documents: "Документы",
    }
    column_searchable_list = [DocumentCategory.name]
    column_details_list = [DocumentCategory.name]
    page_size = 50


class OrganizationDocumentsAdmin(ModelView, model=OrganizationDocument):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "документ"
    name_plural = "Документы организации"
    column_list = [OrganizationDocument.name, OrganizationDocument.file]
    column_labels = {
        OrganizationDocument.name: "Название документа",
        OrganizationDocument.category: "Категория",
        OrganizationDocument.file: "Файл",
        OrganizationDocument.organization_info: "Сведения об организации",
    }
    column_searchable_list = [OrganizationDocument.name]
    column_details_list = [OrganizationDocument.name]
    form_overrides = dict(file=FileField)
    page_size = 50

    async def list(self, request: Request) -> Pagination:
        page = self.validate_page_number(request.query_params.get("page"), 1)
        page_size = self.validate_page_number(request.query_params.get("pageSize"), 0)
        page_size = min(page_size or self.page_size, max(self.page_size_options))
        search = request.query_params.get("search", None)

        stmt = self.list_query(request)
        for relation in self._list_relations:
            stmt = stmt.options(selectinload(relation))

        stmt = self.sort_query(stmt, request)

        if search:
            stmt = self.search_query(stmt=stmt, term=search)
            count = await self.count(request, select(func.count()).select_from(stmt))
        else:
            count = await self.count(request)

        stmt = stmt.limit(page_size).offset((page - 1) * page_size)
        rows = await self._run_query(stmt)
        for row in rows:
            row.file = f"{settings.PRODUCTION_URL}{row.file}"

        pagination = Pagination(
            rows=rows,
            page=page,
            page_size=page_size,
            count=count,
        )

        return pagination
