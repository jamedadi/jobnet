from django_filters import rest_framework as filters

from company.models import Company


class CompanyFilter(filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            'type': ['exact'],
            'city': ['exact'],
        }
