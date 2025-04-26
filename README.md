# Древовидное меню в Django

Реализация древовидного меню в Django

## Как запустить проект

Скачать удаленный репозиторий выполнив команду:

```
git clone https://github.com/AlekseiTolchin/django_tree_menu
```
Docker и Docker-compose должны быть установлены в системе.

Собрать докер-образы:

```
docker-compose build
```

Запустить докер-контейнеры и не выключать:

```
docker-compose up
```

После запуска веб-сервисов с помощью Docker Сompose в новом терминале, не выключая сайт, загрузить в БД тестовые данные:

```
docker-compose exec database psql -U user db -f /test_data/test_data.sql
```
- В базе данных появится одно меню и superuser.
- admin (superuser) - пароль `admin`

При редактировании структуры моделей - накатить миграции с помощью команды:

```
docker-compose run --rm web-app python manage.py migrate
```

Ссылки для тестирования:

- http://127.0.0.1:8000/admin/ - `админ-панель` 
- http://127.0.0.1:8000/ - `главная страница`