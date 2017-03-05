import os
from growbot.celery import *
from django.db import models
from django.db.models import signals
from solo.models import SingletonModel


def itersubclasses(cls, _seen=None):
  if not isinstance(cls, type):
    raise TypeError('itersubclasses must be called with '
                    'new-style classes, not %.100r' % cls)
  if _seen is None: _seen = set()
  try:
    subs = cls.__subclasses__()
  except TypeError:  # fails only when cls is type
    subs = cls.__subclasses__(cls)
  for sub in subs:
    if sub not in _seen:
      _seen.add(sub)
      yield sub
      for sub in itersubclasses(sub, _seen):
        yield sub



class Control(models.Model):
  name      = models.CharField(max_length=32, primary_key=True)
  level     = models.IntegerField(default=0)
  floor     = models.IntegerField(default=0)
  threshold = models.IntegerField(default=255)
  def __str__(self):
    return (self.name)
  def action(self):
    pass
  def fire(self):
    self.action()
  def pollFire(self):
    retval = 'no change'
    if self.level >= self.threshold:
      retval = 'changed'
      self.fire()
    return retval

class InputControl(Control):
  output = models.ForeignKey('OutputControl',null=True)
  def pollFire(self):
    if not self.output == None:
      self.fire()
  def fire(self):
    self.output.level = self.level
    self.output.save()

class OutputControl(Control):
  firing = models.BooleanField(default=False,editable=False)

class FilterControl(OutputControl):
  output = models.ForeignKey('OutputControl',null=True)



## Controls
class Knob(InputControl):
  level = models.IntegerField(default=0)
class PWM(InputControl):
  frequency = models.IntegerField(default=86400)
  width     = models.IntegerField(default=300)
  phase     = models.IntegerField(default=21600)
class LineCross(FilterControl):
  counter = models.IntegerField(default=0,editable=False)
  rise    = models.IntegerField(default=10)
  fall    = models.IntegerField(default=10)
  def pollFire(self):
    retval = 'no change'
    if self.level >= self.threshold and not self.counter >= self.rise:
      self.counter += 1
    elif not self.counter <= (self.fall * -1) and self.firing:
      self.counter -= 1
    if self.counter >= self.rise:
      self.firing = True
    elif self.counter <= (self.fall * -1):
      self.firing = False
      self.counter = 0
    if self.firing:
      retval = 'changed'
      self.fire()
    self.save()
    return retval
  def fire(self):
    if not self.output == None:
      self.output.level = self.level
      self.output.save()
class Logger(OutputControl):
  message = models.CharField(max_length=4096)
  def action(self):
    print self.message
    self.message = 'it worked'
    self.save()






#@periodic_task(run_every=1)
def pollFire():
  for controller in itersubclasses(Control):
    for control in controller.objects.all():
      if 'pollFire' in dir(control):
        print control
        control.pollFire()
