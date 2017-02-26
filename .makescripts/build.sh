#!/usr/bin/env bash
. env/bin/activate
cd GrowBot
python manage.py migrate
python manage.py makemigrations growbot
python manage.py migrate
