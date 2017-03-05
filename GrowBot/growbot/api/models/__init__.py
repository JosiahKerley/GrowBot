from __future__ import unicode_literals
from solo.models import SingletonModel
from camera import *
from automation import *
from powerswitch import *

## Site config model
class SiteConfiguration(SingletonModel):
  site_name = models.CharField(max_length=255, default='Site Name')
  maintenance_mode = models.BooleanField(default=False)
  def __unicode__(self):
    return u"Site Configuration"
  class Meta:
    verbose_name = "Site Configuration"

