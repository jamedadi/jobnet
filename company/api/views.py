from rest_framework.viewsets import ModelViewSet

from company.api.filters import CompanyFilter
from company.api.serializers import CompanySerializer
from company.models import Company

from lib.api.permissions import IsObjectEmployerOrReadOnly


class CompanyModelViewSetAPI(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsObjectEmployerOrReadOnly,)
    filterset_class = CompanyFilter
    search_fields = ('persian_name', 'english_name')

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)
