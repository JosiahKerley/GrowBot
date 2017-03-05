import pytz
import time
import datetime
from django.db import models
from growbot.celery import *
from django.db.models import signals
#from DGIWebPowerSwitch import Control
from solo.models import SingletonModel
from django.core.exceptions import ValidationError


## Tasks
from growbot.api.tasks import *
import dlipower



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
  def __str__(self): return (self.name)
  def __unicode__(self): return (self.name)

  @staticmethod
  def setState(sender, **kwargs):
    try:
      instance = kwargs.get('instance')
      instance.setStateAsync.delay(
        instance.switch.endpoint,
        instance.switch.username,
        instance.switch.password,
        instance.outlet,
        instance.name,
        instance.state
      )
    except: pass

  @staticmethod
  @Async.task()
  def setStateAsync(endpoint,username,password,outlet,name,state):
    wps = dlipower.PowerSwitch(hostname=endpoint.replace('http://',''), userid=username, password=password)
    wps[outlet].name = name
    if state == True:
      print('turning outlet {} on'.format(str(outlet)))
      wps[outlet].on()
    else:
      print('turning outlet {} off'.format(str(outlet)))
      wps[outlet].off()

  @staticmethod
  @periodic_task(run_every=10)
  def getStateAsync():
    power = PowerSwitch.objects.all()[0]
    endpoint = power.endpoint.replace('http://','')
    username = power.username
    password = power.password
    wps = dlipower.PowerSwitch(hostname=endpoint, userid=username, password=password)
    switches = PowerOutlet.objects.all()
    for switch in switches:
      state = str(wps[switch.outlet].state)
      if "ON" in state:
        switch.state = True
      else:
        switch.state = False
      switch.save()


class Switcher(models.Model):
  name = models.CharField(primary_key=True, max_length=128)
  outlet = models.ForeignKey(PowerOutlet)
  def __str__(self): return (self.name)
  def __unicode__(self): return (self.name)

class SimpleTimer(Switcher):
  on    = models.TimeField()
  off   = models.TimeField()
  state = models.BooleanField(default=False,editable=False)

  @staticmethod
  @periodic_task(run_every=10)
  def turnOn():
    timers = SimpleTimer.objects.all()
    for timer in timers:
      outlet = timer.outlet
      on     = timer.on
      off    = timer.off
      now    = datetime.datetime.now(pytz.timezone('MST')).time()
      if on < now and off > now:
        print 'turning on {}'.format(outlet.name)
        timer.state = True
        outlet.state = True
      if on < now and not off > now and timer.state == True:
        print 'turning off {}'.format(outlet.name)
        timer.state = False
        outlet.state = False
      outlet.save()
      timer.save()


## Process signals
signals.post_save.connect(PowerOutlet.setState, sender=PowerOutlet)
