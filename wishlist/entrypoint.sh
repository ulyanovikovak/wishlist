#!/bin/sh
set -e  # Завершает выполнение при ошибке


# Ожидание доступности базы данных
echo " Ожидание базы данных..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  echo " Ожидание базы данных ($DATABASE_HOST:$DATABASE_PORT)..."
  sleep 1
done

echo " База данных доступна!"

# Применение миграций
echo " Применение миграций..."
python manage.py migrate --noinput



# Запуск сервера Django
echo " Запуск сервера Django..."
exec python manage.py runserver 0.0.0.0:8000


