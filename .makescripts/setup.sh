#!/usr/bin/env bash
. env/bin/activate
cd GrowBot
echo "from django.contrib.auth.models import User; User.objects.create_superuser('adminuser', 'adminuser@ctlsdn.io', 'adminpass')" | \
  python manage.py shell
python manage.py migrate
