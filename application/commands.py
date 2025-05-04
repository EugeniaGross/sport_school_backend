import asyncio
import sys

import rich
from litestar.plugins import CLIPluginProtocol
from click import Group

from settings import logger
from users.depenfiences import users_service


class CLIPlugin(CLIPluginProtocol):
    def on_cli_init(self, cli: Group) -> None:
        @cli.command()
        def create_admin():
            email = input("Введите фдрес электронной почты: ")
            password = input("Введите пароль: ")
            confirm_password = input("Повтороите пароль: ")
            if password != confirm_password:
                rich.print("[red]Пароли не совпадают")
                sys.exit(1)
            try:
                asyncio.run(users_service().add_one(email, password))
                rich.print(f"[green]Администратор {email} успешно создан")
            except Exception as e:
                logger.error(e)
                rich.print("[red]Введите корректные данные")
