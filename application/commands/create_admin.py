import asyncio
import pathlib
import sys

import rich

if __name__ == "__main__":
    sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

from users.depenfiences import users_service


async def create_admin():
    email = input("Введите фдрес электронной почты: ")
    password = input("Введите пароль: ")
    confirm_password = input("Повтороите пароль: ")
    if password != confirm_password:
        rich.print("[red]Пароли не совпадают")
        sys.exit(1)
    try:
        await users_service().add_one(email, password)
        rich.print(f"[green]Администратор {email} успешно создан")
    except Exception as e:
        print(e)
        rich.print("[red]Введите корректные данные")
        
        
if __name__ == "__main__":
    asyncio.run(create_admin())
