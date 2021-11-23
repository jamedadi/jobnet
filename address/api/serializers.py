from rest_framework import serializers

from address.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'slug')


class CitySerializer(serializers.ModelSerializer):
    def get_state(self, obj):
        return {
            "name": obj.state.name,
            "slug": obj.sate.slug
        }

    author = serializers.SerializerMethodField('get_state')

    class Meta:
        model = City
        fields = ('name', 'slug')
