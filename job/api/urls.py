from django.urls import path, include
from rest_framework import routers

from job.api.views import JobCategoryViewSet, SkillViewSet, JobViewSet

router = routers.SimpleRouter()
router.register('skill', SkillViewSet)
router.register('job-category', JobCategoryViewSet)
router.register('', JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
