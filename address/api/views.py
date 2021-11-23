from rest_framework.viewsets import ModelViewSet

from address.api.serializers import StateSerializer, ReadCitySerializer, WriteCitySerializer
from address.models import State, City


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WriteCitySerializer
        return ReadCitySerializer
