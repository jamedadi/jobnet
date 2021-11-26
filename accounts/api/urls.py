from django.urls import path, include

from rest_framework import routers

from accounts.api.views import UserRegistrationCreateApiView, UserChangePasswordUpdateApiView, \
    JobSeekerAPIView, EmployerAPIView, UserInfo, VerifyEmail

app_name = 'accounts'

router = routers.SimpleRouter()
router.register('job-seeker', JobSeekerAPIView)
router.register('employer', EmployerAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/<str:user_type>/', UserRegistrationCreateApiView.as_view(), name='registration'),
    path('user/', UserInfo.as_view()),
    path('change-password/', UserChangePasswordUpdateApiView.as_view(), name='change-password'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),

]
