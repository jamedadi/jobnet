from django.urls import path, include
from rest_framework import routers

from company.api.views import CompanyModelViewSetAPI

app_name = 'company'

router = routers.SimpleRouter()
router.register('', CompanyModelViewSetAPI)

urlpatterns = [
    path('', include(router.urls)),
]
