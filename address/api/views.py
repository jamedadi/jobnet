from rest_framework.viewsets import ModelViewSet

from address.api.serializers import StateSerializer, ReadCitySerializer, WriteCitySerializer
from address.models import State, City
from lib.api.permissions import IsAdminOrReadOnly


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['state__name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WriteCitySerializer
        return ReadCitySerializer
