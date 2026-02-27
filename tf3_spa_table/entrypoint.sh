#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.2
done
echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py seed_table_data --count 150
python manage.py collectstatic --noinput

exec "$@"
