from __future__ import absolute_import
import os
from celery import Celery
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growbot.settings')


## Setup celery
Async = Celery('growbot.api', broker=settings.BROKER_URL, backend=settings.BROKER_BACKEND)
Async.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

## Create task decorators et al
from celery.decorators import *

