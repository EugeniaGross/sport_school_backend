from sqladmin import ModelView
from wtforms import TextAreaField

from types_sports.models import TypesSports


class TypesSportsAdmin(ModelView, model=TypesSports):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "вид спорта"
    name_plural = "Виды спорта"
    column_list = [TypesSports.name]
    column_labels = {
        TypesSports.name: "Название",
        TypesSports.description: "Описание",
    }
    column_searchable_list = [TypesSports.name]
    column_details_list = [TypesSports.name]
    form_overrides = dict(description=TextAreaField)
    form_excluded_columns = [
        TypesSports.uncoming_events,
        TypesSports.coaches,
        TypesSports.athletes,
    ]
    page_size = 50
