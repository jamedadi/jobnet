from rest_framework.viewsets import ModelViewSet

from job.api.permissions import IsEmployerOrReadOnly, IsCompanyEmployerOrReadOnly
from job.api.serializers import JobCategorySerializer, SkillSerializer, ReadJobSerializer
from job.models import JobCategory, Skill, Job
from lib.api.permissions import IsAdminOrReadOnly


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly | IsEmployerOrReadOnly]


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = ReadJobSerializer
    permission_classes = [IsCompanyEmployerOrReadOnly]
