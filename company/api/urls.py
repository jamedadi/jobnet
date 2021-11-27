from django.urls import path, include
from rest_framework import routers

from company.api.views import CompanyModelViewSetAPI, CompanyTypeModelViewSetAPI, EmployeeTypeModelViewSetAPI, \
    EmployeeModelViewSetAPI

app_name = 'company'

router = routers.SimpleRouter()

router.register('employee', EmployeeModelViewSetAPI)
router.register('', CompanyModelViewSetAPI)
router.register('type/company', CompanyTypeModelViewSetAPI)
router.register('type/employee', EmployeeTypeModelViewSetAPI)

urlpatterns = [
    path('', include(router.urls)),
]
