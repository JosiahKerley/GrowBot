from rest_framework import serializers
from growbot.api.models import *

class PowerSwitchSerializer(serializers.ModelSerializer):
  class Meta:
    model = PowerSwitch
    fields = '__all__'


class PowerOutletSerializer(serializers.ModelSerializer):
  class Meta:
    model = PowerOutlet
    fields = '__all__'

class CameraSnapshotSerializer(serializers.ModelSerializer):
  class Meta:
    model = CameraSnapshot
    fields = '__all__'


