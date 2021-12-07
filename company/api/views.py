from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from company.api.pagination import CompanyLimitOffsetPagination
from company.api.filters import CompanyFilter
from company.api.serializers import CompanySerializer, CompanyTypeSerializer, EmployeeTypeSerializer, EmployeeSerializer
from company.models import Company, CompanyType, EmployeeType, Employee

from lib.api.permissions import IsObjectEmployerOrReadOnly, IsEmployer, IsEmployerOwnedEmployeeOrReadOnly


class CompanyModelViewSetAPI(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsObjectEmployerOrReadOnly,)
    filterset_class = CompanyFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('persian_name', 'english_name')
    ordering_fields = ('created_time',)
    pagination_class = CompanyLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)


class CompanyTypeModelViewSetAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin, GenericViewSet):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = (IsEmployer,)
    search_fields = ('type',)


class EmployeeTypeModelViewSetAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin, GenericViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    permission_classes = (IsEmployer,)
    search_fields = ('type',)


class EmployeeModelViewSetAPI(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsEmployerOwnedEmployeeOrReadOnly,)

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.user.employer.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.employer.company)
