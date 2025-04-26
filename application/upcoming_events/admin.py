from sqladmin import ModelView
from wtforms import TextAreaField
from upcoming_events.models import UpcommingEvents

from admin_plugin import FileField


class UpcommingEventsAdmin(ModelView, model=UpcommingEvents):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "событие"
    name_plural = "Афиша"
    column_list = [
        UpcommingEvents.name,
        UpcommingEvents.date,
        UpcommingEvents.address,
        UpcommingEvents.type_sport,
    ]
    column_labels = {
        UpcommingEvents.name: "Название",
        UpcommingEvents.date: "Дата",
        UpcommingEvents.address: "Адрес",
        UpcommingEvents.description: "Описание",
        UpcommingEvents.image: "Постер",
        UpcommingEvents.type_sport: "Вид спорта",
    }
    column_searchable_list = [UpcommingEvents.name]
    column_details_list = [
        UpcommingEvents.name,
        UpcommingEvents.date,
        UpcommingEvents.address,
        UpcommingEvents.type_sport,
    ]
    form_overrides = dict(image=FileField, description=TextAreaField)
    page_size = 50
