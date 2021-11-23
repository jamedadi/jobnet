from rest_framework import serializers

from address.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'slug')


class ReadCitySerializer(serializers.ModelSerializer):
    def get_state(self, obj):
        return {
            'name': obj.state.name,
            'slug': obj.state.slug
        }

    state = serializers.SerializerMethodField('get_state')

    class Meta:
        model = City
        fields = ('name', 'slug', 'state')


class WriteCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('state', 'slug', 'name')
