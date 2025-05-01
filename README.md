В корневой папке проекта создать файл .env. Пример содержания .env:</br>
```
CLIENT_URL=http://localhost:5173
ALLOWED_HOSTS=localhost,127.0.0.1

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=sport_school
MYSQL_USER=db_user
MYSQL_PASSWORD=db_user_password
MYSQL_HOST=db
MYSQL_PORT=3306
```

Запуск проекта: docker compose up --build</br>
Для создания администратора ввести следующие команды: </br>
```
docker compose exec backend bash
python application/commands/create_admin.py
```

Панель администратора доступна по адресу: http://localhost:8000/admin</br>

API документация доступна по адресу: http://localhost:8000/documentation