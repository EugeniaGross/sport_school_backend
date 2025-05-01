from users.repository import UsersMySQLRepository
from users.service import UserService


def users_service():
    return UserService(UsersMySQLRepository)
