from sqladmin import ModelView
from athletes.models import Athlet
from admin_plugin import FileField


class AthletesAdmin(ModelView, model=Athlet):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "спортсмена"
    name_plural = "Спортсмены"
    column_list = [
        Athlet.first_name,
        Athlet.last_name,
        Athlet.middle_name,
        Athlet.type_sport,
    ]
    column_labels = {
        Athlet.first_name: "Имя",
        Athlet.last_name: "Фамилия",
        Athlet.middle_name: "Отчество",
        Athlet.qualification: "Звание",
        Athlet.image: "Фотография",
        Athlet.type_sport: "Вид спорта",
    }
    column_searchable_list = [Athlet.last_name, Athlet.first_name]
    column_details_list = [
        Athlet.first_name,
        Athlet.last_name,
        Athlet.middle_name,
        Athlet.type_sport,
    ]
    form_overrides = dict(image=FileField)
    page_size = 50
