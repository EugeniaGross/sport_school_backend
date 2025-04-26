from sqladmin import ModelView
from wtforms import TextAreaField
from coaches.models import Coach
from admin_plugin import FileField


class CoachesAdmin(ModelView, model=Coach):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "тренера"
    name_plural = "Тренеры"
    column_list = [
        Coach.first_name,
        Coach.last_name,
        Coach.middle_name,
        Coach.type_sport,
    ]
    column_labels = {
        Coach.first_name: "Имя",
        Coach.last_name: "Фамилия",
        Coach.middle_name: "Отчество",
        Coach.description: "Описание",
        Coach.image: "Фотография",
        Coach.type_sport: "Вид спорта",
    }
    column_searchable_list = [Coach.last_name, Coach.first_name]
    column_details_list = [
        Coach.first_name,
        Coach.last_name,
        Coach.middle_name,
        Coach.type_sport,
    ]
    form_overrides = dict(image=FileField, description=TextAreaField)
    page_size = 50
