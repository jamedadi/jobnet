from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.api.permissions import IsNotAuthenticated, IsJobSeeker, IsEmployer
from accounts.api.serializers import UserRegistrationSerializer, UserChangePasswordSerializer, \
    JobSeekerSerializer, EmployerSerializer
from accounts.models import JobSeeker, Employer
from rest_framework.exceptions import NotAcceptable

User = get_user_model()


class UserRegistrationCreateApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'employer':
            serializer.save(is_employer=True)
        elif user_type == 'job_seeker':
            serializer.save(is_job_seeker=True)
        raise NotAcceptable


class UserChangePasswordUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class JobSeekerAPIView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = (IsJobSeeker,)


class EmployerAPIView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (IsEmployer,)
