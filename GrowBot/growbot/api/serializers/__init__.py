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

class SimpleTimerSerializer(serializers.ModelSerializer):
  class Meta:
    model = SimpleTimer
    fields = '__all__'



class PWMSerializer(serializers.ModelSerializer):
  class Meta:
    model = PWM
    fields = '__all__'
class KnobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Knob
    fields = '__all__'
class LineCrossSerializer(serializers.ModelSerializer):
  class Meta:
    model = LineCross
    fields = '__all__'
class LoggerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Logger
    fields = '__all__'


