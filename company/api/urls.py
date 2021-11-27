from django.urls import path, include
from rest_framework import routers

from company.api.views import CompanyModelViewSetAPI, CompanyTypeModelViewSetAPI, EmployeeTypeModelViewSetAPI, \
    EmployeeModelViewSetAPI

app_name = 'company'

router = routers.SimpleRouter()

router.register('employee', EmployeeModelViewSetAPI)
router.register('company-type', CompanyTypeModelViewSetAPI)
router.register('employee-type', EmployeeTypeModelViewSetAPI)
router.register('', CompanyModelViewSetAPI)

urlpatterns = [
    path('', include(router.urls)),
]
