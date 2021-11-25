from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import CreateAPIView
from rest_framework import exceptions

from accounts.api.permissions import IsNotAuthenticated
from accounts.api.serializers import UserRegistrationSerializer

User = get_user_model()


class UserRegistrationCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated, )
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'is_employer':
            serializer.save(is_employer=True)
        elif user_type == 'is_job_seeker':
            serializer.save(is_job_seeker=True)
        else:
            raise exceptions.NotAcceptable(_('Don\'t send bad params!'))


