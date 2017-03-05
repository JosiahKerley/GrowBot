from rest_framework import viewsets
from growbot.api.models import *
from growbot.api.serializers import *

class PowerSwitchViewSet(viewsets.ModelViewSet):
  queryset = PowerSwitch.objects.all()
  serializer_class = PowerSwitchSerializer

class PowerOutletViewSet(viewsets.ModelViewSet):
  queryset = PowerOutlet.objects.all()
  serializer_class = PowerOutletSerializer

class CameraSnapshotViewSet(viewsets.ModelViewSet):
  queryset = CameraSnapshot.objects.all()
  serializer_class = CameraSnapshotSerializer

class SimpleTimerViewSet(viewsets.ModelViewSet):
  queryset = SimpleTimer.objects.all()
  serializer_class = SimpleTimerSerializer



class PWMViewSet(viewsets.ModelViewSet):
  queryset = PWM.objects.all()
  serializer_class = PWMSerializer
class KnobViewSet(viewsets.ModelViewSet):
  queryset = Knob.objects.all()
  serializer_class = KnobSerializer
class LineCrossViewSet(viewsets.ModelViewSet):
  queryset = LineCross.objects.all()
  serializer_class = LineCrossSerializer
class LoggerViewSet(viewsets.ModelViewSet):
  queryset = Logger.objects.all()
  serializer_class = LoggerSerializer




