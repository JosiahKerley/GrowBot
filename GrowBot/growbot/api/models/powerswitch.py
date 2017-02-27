from django.db import models
from growbot.celery import *
from django.db.models import signals
from DGIWebPowerSwitch import Control
from solo.models import SingletonModel
from django.core.exceptions import ValidationError


## Tasks
from growbot.api.tasks import *


class PowerSwitch(SingletonModel):
  endpoint = models.URLField(max_length=200)
  username = models.CharField(max_length=32)
  password = models.CharField(max_length=32)
  def __str__(self):
    return (self.endpoint)


class PowerOutlet(models.Model):
  outlet = models.AutoField(primary_key=True)
  switch = models.ForeignKey(PowerSwitch)
  state  = models.BooleanField(default=False)
  name   = models.CharField(default='',max_length=128)
  def __str__(self):
    return (self.outlet)

  @staticmethod
  def updateSwitch(sender, **kwargs):
    try:
      instance = kwargs.get('instance')
      instance.performSwitchUpdate.delay(
        instance.switch.endpoint,
        instance.switch.username,
        instance.switch.password,
        instance.outlet,
        instance.state
      )
    except: pass

  @staticmethod
  @Async.task()
  def performSwitchUpdate(endpoint,username,password,outlet,state):
    wps = Control(username=username, password=password,
                  endpoint=endpoint)
    try: print(wps.switch(outlet, state))
    except: pass




## Process signals
signals.post_init.connect(PowerOutlet.updateSwitch, sender=PowerOutlet)
signals.post_save.connect(PowerOutlet.updateSwitch, sender=PowerOutlet)