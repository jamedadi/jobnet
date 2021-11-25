from django.urls import path, include

from rest_framework import routers

from resume.api.views import ResumeModelViewSetApi

app_name = 'resume'

router = routers.SimpleRouter()
router.register('', ResumeModelViewSetApi)

urlpatterns = [
    path('', include(router.urls)),
]
