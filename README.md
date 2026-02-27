# 📊 SPA Table Application

Веб-приложение для управления таблицей с Single Page Application интерфейсом. Проект разработан в качестве дипломной работы.

## 🚀 Функциональность
- ✅ **4 колонки**: Дата, Название, Количество, Расстояние
- ✅ **Сортировка** по всем полям, кроме даты
- ✅ **Фильтрация** с выбором колонки и условия (равно, содержит, больше, меньше)
- ✅ **Пагинация** на стороне сервера (10 записей на страницу)
- ✅ **150 тестовых записей** при старте
- ✅ **Docker** контейнеризация
- ✅ **Swagger** документация API
- ✅ **CORS** настроен

## 🛠 Технологический стек
### Backend
- Python 3.13
- Django 4.2.16
- Django REST Framework
- PostgreSQL / SQLite
- django-filter
- drf-spectacular (Swagger)

### Frontend
- React 18
- Axios
- Bootstrap 5

### Инфраструктура
- Docker + Docker Compose
- Nginx
- Git + GitHub

## 📦 Установка и запуск
### Локальный запуск
```bash
git clone git@github.com:ZhannaIvanova10/tf3_spa_table.git
cd tf3_spa_table
python -m venv venv
source venv/Scripts/activate  # для Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_table_data --count 150
cd frontend
npm install
npm run build
cd ..
python manage.py runserver