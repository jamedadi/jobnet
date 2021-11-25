from rest_framework import serializers

from address.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name', 'slug')


class ReadCitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = ('name', 'slug', 'state')


class WriteCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('state', 'slug', 'name')
