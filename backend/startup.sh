#!/bin/bash

echo "--- Running collectstatic ---"
python manage.py collectstatic --noinput

echo "--- Running migrations ---"
python manage.py migrate --noinput

echo "--- Starting Gunicorn ---"
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 core.wsgi
