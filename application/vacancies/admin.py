from sqladmin import ModelView
from wtforms import TextAreaField

from vacancies.models import Vacancy


class VacanciesAdmin(ModelView, model=Vacancy):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "вакансия"
    name_plural = "Вакансии"
    column_list = [Vacancy.name]
    column_labels = {
        Vacancy.name: "Название",
        Vacancy.description: "Описание",
        Vacancy.email: "Электроная почта для связи",
        Vacancy.phone: "Телефон для связи",
    }
    column_searchable_list = [Vacancy.name]
    column_details_list = [Vacancy.name]
    form_overrides = dict(description=TextAreaField)
    page_size = 50
