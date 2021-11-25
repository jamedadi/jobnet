from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from accounts.api.permissions import IsNotAuthenticated, UserObjectOwner
from accounts.api.serializers import UserRegistrationSerializer, UserChangePasswordSerializer, \
    UserDetailUpdateAndReadSerializer

User = get_user_model()


class UserRegistrationCreateApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'is_employer':
            serializer.save(is_employer=True)
        elif user_type == 'is_job_seeker':
            serializer.save(is_job_seeker=True)
        else:
            raise exceptions.NotAcceptable(_('Don\'t send bad params!'))


class UserChangePasswordUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserUpdateDetailUpdateApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailUpdateAndReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            permission_classes = (UserObjectOwner,)
        else:
            permission_classes = ()
        return (permission() for permission in permission_classes)
