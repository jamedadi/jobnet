from django.urls import path, include
from rest_framework import routers

from company.api.views import CompanyModelViewSetApi

app_name = 'company'

router = routers.SimpleRouter()
router.register('', CompanyModelViewSetApi)

urlpatterns = [
    path('', include(router.urls)),
]
