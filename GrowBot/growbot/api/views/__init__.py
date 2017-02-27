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




