import os
import commands
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="test",
    ignore_result=True
)
def test():
  logger.info("findme")

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="foobar",
    ignore_result=True
)
def foobar():
  print commands.getstatusoutput('date > /tmp/test')

