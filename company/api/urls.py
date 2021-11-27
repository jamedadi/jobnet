from django.urls import path, include
from rest_framework import routers

from company.api.views import CompanyModelViewSetAPI, CompanyTypeModelViewSetAPI

app_name = 'company'

router = routers.SimpleRouter()
router.register('type', CompanyTypeModelViewSetAPI)
router.register('', CompanyModelViewSetAPI)

urlpatterns = [
    path('', include(router.urls)),
]
