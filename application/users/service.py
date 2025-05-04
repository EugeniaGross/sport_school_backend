from users.exeptions import UserNotFoundError, VerifyPasswordError
from users.repository import UsersAbstractRepository
from users.utils import create_hash_password, verify_password


class UserService:

    def __init__(self, repo: UsersAbstractRepository):
        self.repo: UsersAbstractRepository = repo

    async def add_one(self, email, password):
        hash_password = create_hash_password(password)
        await self.repo.add_one({"email": email, "hash_password": hash_password})

    async def get_one(self, id: int):
        return await self.repo.get_one(id)

    async def get_one_by_email(self, email: str):
        return await self.repo.get_one_by_email(email)

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_one_by_email(email)
        if user is None:
            raise UserNotFoundError("Пользователь не найден")
        if not verify_password(password, user.hash_password):
            raise VerifyPasswordError("Пароль введен не верно")
        return user
