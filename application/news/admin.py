from sqladmin import ModelView
from wtforms import TextAreaField
from news.models import News, PhotoNews

from admin_plugin import FileField


class NewsAdmin(ModelView, model=News):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "новость"
    name_plural = "Новости"
    column_list = [
        News.name,
        News.date,
        News.address,
        News.type_sport,
    ]
    column_labels = {
        News.name: "Название",
        News.date: "Дата",
        News.address: "Адрес",
        News.description: "Описание",
        News.image: "Постер",
        News.type_sport: "Вид спорта",
        News.photos: "Фотографии",
    }
    column_searchable_list = [News.name]
    column_details_list = [
        News.name,
        News.date,
        News.address,
        News.type_sport,
    ]
    form_overrides = dict(image=FileField, description=TextAreaField)
    page_size = 50


class PhotoNewsAdmin(ModelView, model=PhotoNews):
    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    name = "фотографию"
    name_plural = "Фотографии для новостей"
    column_list = [
        PhotoNews.news,
        PhotoNews.image,
    ]
    column_labels = {
        PhotoNews.news: "Новость",
        PhotoNews.image: "Фотография",
    }
    column_searchable_list = [PhotoNews.news]
    column_details_list = [
        PhotoNews.news,
        PhotoNews.image,
    ]
    form_overrides = dict(image=FileField)
    page_size = 50
