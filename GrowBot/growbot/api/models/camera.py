import os
from django.db import models
from growbot.celery import *
from django.conf import settings
from django.core.files import File
from django.db.models import signals
from solo.models import SingletonModel
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

## Tasks
from growbot.api.tasks import *


## Validators
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class CameraSnapshot(models.Model):
  default   = 'http://icons.iconarchive.com/icons/chrisbanks2/cold-fusion-hd/128/youtube-black-wait-icon.png'
  camera    = models.IntegerField(primary_key=True)
  imagename = models.CharField(max_length=128,unique=True, validators=[alphanumeric])
  image     = models.ImageField(upload_to=settings.MEDIA_ROOT,default=default)
  def __str__(self):
    return (self.imagename)


  @staticmethod
  def updateCamera(sender, **kwargs):
    try:
      instance = kwargs.get('instance')
      abspath = os.path.join(settings.BASE_DIR, os.path.join(settings.MEDIA_ROOT, str(instance.imagename) + '.png'))
      instance.takeSnapshot.delay(abspath,instance.camera)
      instance.image.save(abspath,File(open(abspath),'r'))
      instance.save()
    except:
      pass

  @staticmethod
  def seedImage(sender, **kwargs):
    instance = kwargs.get('instance')
    abspath = os.path.join(settings.BASE_DIR, os.path.join(settings.MEDIA_ROOT, str(instance.imagename) + '.png'))
    if os.path.isfile(instance.default) and not os.path.isfile(abspath):
      with open(instance.default,'rwb') as src:
        with open(abspath, 'rwb') as dest:
          dest.write(src.read())


  @staticmethod
  @Async.task()
  def takeSnapshot(imagename,camera):
    import pygame.camera
    import pygame.image
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[camera])
    cam.start()
    try:
      img = cam.get_image()
      if os.path.isfile(imagename):
        os.remove(imagename)
      pygame.image.save(img, imagename)
      cam.stop()
    except:
      pass
    pygame.camera.quit()


## Process signals
signals.post_init.connect(CameraSnapshot.updateCamera, sender=CameraSnapshot)
signals.post_save.connect(CameraSnapshot.seedImage, sender=CameraSnapshot)
