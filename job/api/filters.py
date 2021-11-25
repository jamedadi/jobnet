from django_filters import rest_framework as filters
from job.models import Job


class JobFilter(filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            'category__name': ['exact'],
            'city__name': ['exact'],
            'city__state__name': ['exact'],
            'cooperation_type': ['exact'],
            'remote_available': ['exact'],
            'salary': ['lt', 'gt']
        }
