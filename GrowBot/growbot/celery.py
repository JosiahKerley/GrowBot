from __future__ import absolute_import
import os
from celery import Celery
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growbot.settings')
app = Celery('growbot.api', broker=settings.BROKER_URL, backend=settings.BROKER_BACKEND)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



