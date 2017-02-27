from __future__ import absolute_import, unicode_literals
import time
from .celery import app as Async
__all__ = ['Async']




@Async.task
def testTask(string):
  print string

Async.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'growbot.api.testTask',
        'schedule': 10.0,
        'args': ('>>>>>>>-<<<<<<<')
    },
}
Async.conf.timezone = 'UTC'


