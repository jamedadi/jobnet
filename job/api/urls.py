from django.urls import path, include
from rest_framework import routers

from job.api.views import JobCategoryViewSet, SkillViewSet, JobViewSet

router = routers.SimpleRouter()
router.register('skill', SkillViewSet)
router.register('', JobViewSet)
router.register('job-category', JobCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
