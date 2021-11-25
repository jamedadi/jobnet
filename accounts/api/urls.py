from django.urls import path

from accounts.api.views import UserRegistrationCreateApiView

app_name = 'accounts'

urlpatterns = [
    path('registration/<str:user_type>/', UserRegistrationCreateApiView.as_view(), name='registration'),
]
