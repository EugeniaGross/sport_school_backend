from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any
import os
import io

import sqladmin
from litestar.types.empty import Empty
from litestar.utils.empty import value_or_default
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.datastructures import URL, FormData, UploadFile
from sqladmin.helpers import get_object_identifier
from sqladmin_litestar_plugin import SQLAdminPlugin, PathFixMiddleware
from starlette.responses import RedirectResponse, Response
from sqladmin.authentication import AuthenticationBackend, login_required
from starlette.exceptions import HTTPException
from markupsafe import Markup
from wtforms import Field, widgets
from starlette.requests import Request
from starlette.responses import RedirectResponse

from settings import settings
from users.depenfiences import users_service
from users.utils import create_jwt_token, decode_jwt_token

if TYPE_CHECKING:
    from collections.abc import Sequence

    from litestar.types.empty import EmptyType
    from sqladmin import ModelView
    from sqladmin.authentication import AuthenticationBackend
    from sqlalchemy.engine import Engine
    from sqlalchemy.ext.asyncio import AsyncEngine
    from sqlalchemy.orm import sessionmaker
    from starlette.middleware import Middleware


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["email"], form["password"]
        try:
            user = await users_service().authenticate_user(email, password)
            request.session.update(
                {
                    "token": create_jwt_token(
                        {"id": user.id}, settings.ADMIN_TOKEN_EXPIRE_DAYS
                    )
                }
            )
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token or (decode_token := decode_jwt_token(token)) is None:
            return False
        user = await users_service().get_one(decode_token["id"])
        if user is None:
            return False
        return True


class SQLAdmin(sqladmin.Admin):
    
    @login_required
    async def list(self, request: Request) -> Response:
        """List route to display paginated Model instances."""

        await self._list(request)

        model_view = self._find_model_view(request.path_params["identity"])
        pagination = await model_view.list(request)
        pagination.add_pagination_urls(request.url)

        request_page = model_view.validate_page_number(
            request.query_params.get("page"), 1
        )

        if request_page > pagination.page:
            return RedirectResponse(
                request.url.include_query_params(page=pagination.page), status_code=302
            )

        context = {
            "model_view": model_view, 
            "pagination": pagination, 
            "prod_url": settings.PRODUCTION_URL
        }
        return await self.templates.TemplateResponse(
            request, model_view.list_template, context
        )

    @login_required
    async def details(self, request: Request) -> Response:
        """Details route."""

        await self._details(request)

        model_view = self._find_model_view(request.path_params["identity"])

        model = await model_view.get_object_for_details(request.path_params["pk"])
        if not model:
            raise HTTPException(status_code=404)

        context = {
            "model_view": model_view,
            "model": model,
            "title": model_view.name,
            "prod_url": settings.PRODUCTION_URL
        }

        return await self.templates.TemplateResponse(
            request, model_view.details_template, context
        )

    @login_required
    async def index(self, request: Request) -> Response:
        return await self.templates.TemplateResponse(
            request, 
            "index.html", 
            {"prod_url": settings.PRODUCTION_URL}
        )

    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        context = {"prod_url": settings.PRODUCTION_URL}
        if request.method == "GET":
            return await self.templates.TemplateResponse(
                request, 
                "login.html",
                context
            )

        ok = await self.authentication_backend.login(request)
        if not ok:
            context["error"] = "Некорректные данные"
            return await self.templates.TemplateResponse(
                request, "login.html", context, status_code=400
            )

        return RedirectResponse(
            request.url_for("admin:index"), status_code=302
        )

    async def _handle_form_data(
        self, request: Request, obj: Any = None
    ) -> FormData:
        """
        Handle form data and modify in case of UploadFile.
        This is needed since in edit page
        there's no way to show current file of object.
        """
        form = await request.form()
        form_data: list[tuple[str, str | UploadFile]] = []
        for key, value in form.multi_items():
            if not isinstance(value, UploadFile):
                form_data.append((key, value))
                continue

            should_clear = form.get(key + "_checkbox")
            empty_upload = len(await value.read(1)) != 1
            await value.seek(0)
            if should_clear:
                form_data.append((key, UploadFile(io.BytesIO(b""))))
            elif empty_upload and obj and getattr(obj, key):
                form_data.append((key, getattr(obj, key)))
            else:
                form_data.append((key, value))
        return FormData(form_data)

    async def save_file(self, file: UploadFile, type: str):
        with open(
            os.path.join(
                settings.BASE_DIR, "statics", f"{type}", file.filename
            ),
            "wb",
        ) as f:
            f.write(file.file.read())
        return f"/statics/{type}/{file.filename}"

    @login_required
    async def create(self, request: Request) -> Response:
        """Create model endpoint."""

        await self._create(request)

        identity = request.path_params["identity"]
        model_view = self._find_model_view(identity)

        Form = await model_view.scaffold_form(model_view._form_create_rules)
        form_data = await self._handle_form_data(request)
        form = Form(form_data)

        context = {
            "model_view": model_view,
            "form": form,
            "prod_url": settings.PRODUCTION_URL
        }

        if request.method == "GET":
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context
            )

        if not form.validate():
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context, status_code=400
            )

        form_data_dict = self._denormalize_wtform_data(
            form.data, model_view.model
        )
        if "image" in form_data_dict:
            image = form_data_dict["image"]
            file_name = await self.save_file(image, "images")
            form_data_dict["image"] = file_name
        if "file" in form_data_dict:
            image = form_data_dict["file"]
            file_name = await self.save_file(image, "documents")
            form_data_dict["file"] = file_name
        try:
            obj = await model_view.insert_model(request, form_data_dict)
        except Exception as e:
            logging.exception(e)
            context["error"] = str(e)
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context, status_code=400
            )

        url = self.get_save_redirect_url(
            request=request,
            form=form_data,
            obj=obj,
            model_view=model_view,
        )
        return RedirectResponse(url=url, status_code=302)

    @login_required
    async def edit(self, request: Request) -> Response:
        """Edit model endpoint."""

        await self._edit(request)

        identity = request.path_params["identity"]
        model_view = self._find_model_view(identity)

        model = await model_view.get_object_for_edit(request)
        if not model:
            raise HTTPException(status_code=404)

        Form = await model_view.scaffold_form(model_view._form_edit_rules)

        context = {
            "obj": model,
            "model_view": model_view,
            "form": Form(obj=model, data=self._normalize_wtform_data(model)),
            "prod_url": settings.PRODUCTION_URL
        }

        if request.method == "GET":
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context
            )

        form_data = await self._handle_form_data(request, model)

        form = Form(form_data)
        if not form.validate():
            context["form"] = form
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context, status_code=400
            )

        form_data_dict = self._denormalize_wtform_data(form.data, model)
        if "image" in form_data_dict and isinstance(
            image := form_data_dict["image"], UploadFile
        ):
            file_name = await self.save_file(image, "images")
            form_data_dict["image"] = file_name
        if "file" in form_data_dict and isinstance(
            file := form_data_dict["file"], UploadFile
        ):
            file_name = await self.save_file(file, "documents")
            form_data_dict["file"] = file_name
        try:
            if model_view.save_as and form_data.get("save") == "Save as new":
                obj = await model_view.insert_model(request, form_data_dict)
            else:
                obj = await model_view.update_model(
                    request, pk=request.path_params["pk"], data=form_data_dict
                )
        except Exception as e:
            logging.error(e)
            context["error"] = str(e)
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context, status_code=400
            )

        url = self.get_save_redirect_url(
            request=request,
            form=form_data,
            obj=obj,
            model_view=model_view,
        )
        return RedirectResponse(url=url, status_code=302)

    def get_save_redirect_url(
        self, request: Request, form: FormData, model_view: ModelView, obj: Any
    ) -> str | URL:
        """
        Get the redirect URL after a save action
        which is triggered from create/edit page.
        """
        identity = request.path_params["identity"]
        identifier = get_object_identifier(obj)

        if form.get("save") == "Сохранить":
            return request.url_for("admin:list", identity=identity)
        elif form.get("save") == "Сохранить и продолжить редактирование" or (
            form.get("save") == "Сохранить как новый объект"
            and model_view.save_as_continue
        ):
            return request.url_for(
                "admin:edit", identity=identity, pk=identifier
            )
        return request.url_for("admin:create", identity=identity)


class AdminPlugin(SQLAdminPlugin):
    def __init__(  # noqa: PLR0913
        self,
        *,
        views: Sequence[type[ModelView]] | EmptyType = Empty,
        engine: Engine | AsyncEngine | EmptyType = Empty,
        sessionmaker: sessionmaker[Any] | EmptyType = Empty,
        base_url: str | EmptyType = Empty,
        title: str | EmptyType = Empty,
        logo_url: str | EmptyType = Empty,
        templates_dir: str | EmptyType = Empty,
        middlewares: Sequence[Middleware] | EmptyType = Empty,
        authentication_backend: AuthenticationBackend | EmptyType = Empty,
    ) -> None:
        """Initializes the SQLAdminPlugin.

        Args:
            views: A sequence of ModelView classes to add to the admin app.
            engine: An SQLAlchemy engine.
            sessionmaker: An SQLAlchemy sessionmaker.
            base_url: The base URL for the admin app.
            title: The title of the admin app.
            logo_url: The URL of the logo to display in the admin app.
            templates_dir: The directory containing the Jinja2 templates for the admin app.
            middlewares: A sequence of Starlette middlewares to add to the admin app.
            authentication_backend: An authentication backend to use for the admin app.
        """
        self.views = list(value_or_default(views, []))
        admin_kwargs = {
            kw: value
            for kw, value in [
                ("engine", engine),
                ("sessionmaker", sessionmaker),
                ("base_url", base_url),
                ("title", title),
                ("logo_url", logo_url),
                ("templates_dir", templates_dir),
                ("middlewares", middlewares),
                ("authentication_backend", authentication_backend),
            ]
            if value is not Empty
        }
        self.starlette_app = Starlette()
        self.admin = SQLAdmin(app=self.starlette_app, **admin_kwargs)  # type: ignore[arg-type]
        self.starlette_app.add_middleware(
            PathFixMiddleware, base_url=self.admin.base_url
        )
        # disables redirecting based on absence/presence of trailing slashes
        self.starlette_app.router.redirect_slashes = False
        self.admin.admin.router.redirect_slashes = False


class FileInputWidget(widgets.FileInput):
    """
    File input widget with clear checkbox.
    """

    def __call__(self, field: Field, **kwargs: Any) -> str:
        if not field.flags.required:
            checkbox_id = f"{field.id}_checkbox"
            checkbox_label = Markup(
                f'<label class="form-check-label" for="{checkbox_id}">Clear</label>'
            )
            checkbox_input = Markup(
                f'<input class="form-check-input" type="checkbox" id="{checkbox_id}" name="{checkbox_id}">'  # noqa: E501
            )
            checkbox = Markup(
                f'<div class="form-check">{checkbox_input}{checkbox_label}</div>'
            )
        else:
            checkbox = Markup()

        if field.data:
            current_value = Markup(
                f"<p>Текущий файл: <a href='{settings.PRODUCTION_URL}{field.data}' target='_blank'>{field.data.split("/")[-1]}</a></p>"
            )
            field.flags.required = False
            return current_value + checkbox + super().__call__(field, **kwargs)
        else:
            return super().__call__(field, **kwargs)


class FileField(Field):

    widget = FileInputWidget()

    def _value(self):
        return False
