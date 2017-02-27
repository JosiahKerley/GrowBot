#!/usr/bin/env bash
. env/bin/activate
cd GrowBot
python manage.py migrate
python manage.py makemigrations growbot
python manage.py migrate
python manage.py migrate django_celery_results
if ! yes|python manage.py collectstatic
then
  echo could not collect static files
fi
