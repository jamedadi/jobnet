from rest_framework import serializers

from address.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('state', 'name')
