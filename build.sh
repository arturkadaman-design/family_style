#!/usr/bin/env bash
# Выходим при ошибке
set -o errexit

# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статику (CSS, картинки)
python manage.py collectstatic --no-input

# Применяем миграции
python manage.py migrate
