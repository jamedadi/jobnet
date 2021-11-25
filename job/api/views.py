from rest_framework.viewsets import ModelViewSet

from job.api.filters import JobFilter
from lib.api.permissions import IsEmployerOrReadOnly, IsObjectEmployerOrReadOnly
from job.api.serializers import JobCategorySerializer, SkillSerializer, ReadJobSerializer, WriteJobSerializer
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
    permission_classes = [IsObjectEmployerOrReadOnly]
    filterset_class = JobFilter
    search_fields = ['title', 'required_skills__title']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return WriteJobSerializer
        return ReadJobSerializer

    def perform_create(self, serializer):
        employer = self.request.user.employer
        serializer.save(employer=employer, company=employer.company)
