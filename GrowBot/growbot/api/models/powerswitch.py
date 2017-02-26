from django.db import models
from django.db.models import signals
from DGIWebPowerSwitch import Control
from solo.models import SingletonModel
from django.core.exceptions import ValidationError

class PowerSwitch(SingletonModel):
  endpoint = models.URLField(max_length=200)
  username = models.CharField(max_length=32)
  password = models.CharField(max_length=32)
  def __str__(self):
    return (self.endpoint)


class PowerOutlet(models.Model):
  outlet = models.AutoField(primary_key=True)
  switch = models.ForeignKey(PowerSwitch)
  state = models.BooleanField(default=False)
  def __str__(self):
    return (self.outlet)

  @staticmethod
  def updateSwitch(sender, **kwargs):
    instance = kwargs.get('instance')
    wps = Control(username=instance.switch.username, password=instance.switch.password,
                  endpoint=instance.switch.endpoint)
    wps.switch(instance.outlet, instance.state)




## Process signals
signals.post_init.connect(PowerOutlet.updateSwitch, sender=PowerOutlet)
