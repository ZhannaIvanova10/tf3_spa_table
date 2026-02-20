#!/bin/sh

# Ждем, пока PostgreSQL запустится
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

# Применяем миграции
python manage.py migrate

# Создаем суперпользователя (если нет)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
"

# Собираем статические файлы
python manage.py collectstatic --noinput

# Запускаем сервер
exec "$@"