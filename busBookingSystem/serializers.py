from rest_framework import serializers

from .models import DestinationState, StateBus


class DestinationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationState
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateBus
        fields = '__all__'        