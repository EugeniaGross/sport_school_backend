В корневой папке проекта создать файл .env. Пример содержания .env:</br>
```
CLIENT_URL=http://localhost:5173
ALLOWED_HOSTS=localhost,127.0.0.1
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "123456789"
ADMIN_TOKEN_EXPIRE_DAYS = 1
SECRET_KEY=12345678

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=sport_school
MYSQL_USER=db_user
MYSQL_PASSWORD=db_user_password
MYSQL_HOST=db
MYSQL_PORT=3306

PRODUCTION_URL = http://localhost:8000

EMAIL_HOST_PASSWORD=xxxxxxxxxxxx
EMAIL_HOST = xxxxxxxxxxxxx
EMAIL_PORT = 587
EMAIL_HOST_USER=xxxxxxxxxxxxx

ADMIN_EMAIL = test@yandex.ru
```

Запуск проекта: </br>
```
docker compose up --build
```
Для создания администратора ввести следующие команды: </br>
```
docker compose exec backend bash
cd application/
litestar create-admin
```

Панель администратора доступна по адресу: http://localhost:8000/admin</br>

API документация доступна по адресу: http://localhost:8000/documentation
