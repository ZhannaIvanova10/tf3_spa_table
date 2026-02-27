# SPA Table (Django + DRF + React)

Проект реализует таблицу в формате SPA с серверной пагинацией, фильтрацией и сортировкой.

## Что реализовано по ТЗ

- Таблица на 4 колонки: `Дата`, `Название`, `Количество`, `Расстояние`.
- SPA-интерфейс на React (без готовых табличных компонентов).
- Сортировка по `Название`, `Количество`, `Расстояние` (без сортировки по дате).
- Фильтрация через:
  - выпадающий список колонки;
  - выпадающий список условий (`eq`, `contains`, `gt`, `lt`);
  - текстовое поле значения.
- Серверная пагинация через DRF.
- Автозаполнение БД случайными данными при старте контейнера.
- Контейнеризация Docker + PostgreSQL + Nginx.
- Nginx проксирует API (backend) и раздаёт frontend.
- Swagger документация: `/api/docs/`.
- CORS настраивается переменной `CORS_ALLOWED_ORIGINS`.

## Стек

- Python 3.11
- Django 4.2 + DRF
- PostgreSQL
- Django ORM
- React + Axios + Bootstrap
- Nginx
- Docker / Docker Compose

## Структура проекта

- `config/` — настройки Django, маршруты.
- `table/` — модель, API, тесты, seed-команда.
- `templates/index.html` — SPA-страница.
- `static/js/app.jsx` — React логика таблицы.
- `static/css/style.css` — стили.
- `docker-compose.yml` — сервисы `db`, `web`, `nginx`.
- `nginx.conf` — проксирование и раздача фронтенда.

## Запуск

```bash
docker compose up --build
```

После старта:

- Frontend: `http://localhost/`
- API: `http://localhost/api/items/`
- Swagger: `http://localhost/api/docs/`

## API фильтрации/сортировки/пагинации

`GET /api/items/`

Параметры:

- `page`, `page_size`
- `ordering`: `name`, `-name`, `quantity`, `-quantity`, `distance`, `-distance`
- `filter_column`: `date | name | quantity | distance`
- `filter_condition`: `eq | contains | gt | lt`
- `filter_value`: строковое значение

Пример:

```bash
curl "http://localhost/api/items/?ordering=-quantity&filter_column=name&filter_condition=contains&filter_value=Маршрут&page=1"
```

## Тесты и покрытие

```bash
coverage run manage.py test
coverage report
```

Целевой порог покрытия: не менее 75%.
