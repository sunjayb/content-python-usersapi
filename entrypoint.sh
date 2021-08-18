#!/bin/sh

echo "Loading PostgreSQL..."

while ! nc -z api-db 5432; do
  sleep 0.1
done

echo "PostgreSQL loaded"

python manage.py run -h 0.0.0.0
