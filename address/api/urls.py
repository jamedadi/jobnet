from django.urls import path, include
from rest_framework import routers

from address.api.views import StateViewSet, CityViewSet

router = routers.SimpleRouter()
router.register('state', StateViewSet)
router.register('city', CityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
