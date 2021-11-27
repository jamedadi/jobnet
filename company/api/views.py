from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from company.api.filters import CompanyFilter
from company.api.serializers import CompanySerializer, CompanyTypeSerializer
from company.models import Company, CompanyType

from lib.api.permissions import IsObjectEmployerOrReadOnly, IsEmployer


class CompanyModelViewSetAPI(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsObjectEmployerOrReadOnly,)
    filterset_class = CompanyFilter
    search_fields = ('persian_name', 'english_name')

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)


class CompanyTypeModelViewSetAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin, GenericViewSet):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = (IsEmployer,)
    search_fields = ('type', )
