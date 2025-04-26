from sqladmin import ModelView
from sqladmin._queries import Query
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
        Organization.name: "Название организации",
        Organization.image: "Постер",
        Organization.email: "Электронная почта",
        Organization.address: "Адрес",
        Organization.phones: "Номера телефонов",
        Organization.telegram_link: "Телеграм",
        Organization.vk_link: "В контакте",
        Organization.whats_app_link: "WhatsApp",
        Organization.rutube_link: "Rutube",
        Organization.sport_objects: "Спортивные объекты",
    }
    column_details_list = [Organization.name]
    form_overrides = dict(image=FileField)
    page_size = 50


class OrganizationPhoneAdmin(ModelView, model=OrganizationPhone):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "телефон"
    name_plural = "Телефоны организации"
    column_list = [
        OrganizationPhone.phone,
    ]
    column_labels = {
        OrganizationPhone.organization: "Организация",
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
        OrganizationSportObject.start_works: "Время начала работы",
        OrganizationSportObject.end_works: "Время окончания работы",
        OrganizationSportObject.organization: "Организация",
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
    column_list = [
        OrganizationDocument.name,
    ]
    column_labels = {
        OrganizationDocument.name: "Название документа",
        OrganizationDocument.category: "Категория",
        OrganizationDocument.file: "Имя файла",
        OrganizationDocument.organization_info: "Сведения об организации",
    }
    column_searchable_list = [OrganizationDocument.name]
    column_details_list = [OrganizationDocument.name]
    form_overrides = dict(file=FileField)
    page_size = 50
