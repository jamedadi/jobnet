from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.permissions import IsNotAuthenticated, IsJobSeeker, IsEmployer
from accounts.api.serializers import UserRegistrationSerializer, UserChangePasswordSerializer, \
    JobSeekerSerializer, EmployerSerializer, UserInfoSerializer, CustomTokenObtainPairSerializer, ResendEmailSerializers
from accounts.models import JobSeeker, Employer
from rest_framework.exceptions import NotAcceptable

from accounts.tasks import send_verification_email_task

User = get_user_model()


class UserRegistrationCreateApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'employer':
            user = serializer.save(is_employer=True)
            send_verification_email_task.delay(user.pk)
        elif user_type == 'job-seeker':
            user = serializer.save(is_job_seeker=True)
            send_verification_email_task.delay(user.pk)
        else:
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


class UserInfo(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyEmail(APIView):
    permission_classes = [IsNotAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        confirmation_token = request.query_params.get('confirmation_token', None)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response('Token is invalid or expired. Please request another confirmation email by signing in.',
                            status=status.HTTP_400_BAD_REQUEST)
        user.email_verified = True
        user.save()
        return Response('Email successfully confirmed')


class ResendEmail(APIView):
    serializer_class = ResendEmailSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User with this email has not been found', status=status.HTTP_404_NOT_FOUND)
        if not user.email_verified:
            send_verification_email_task.delay(user.pk)
            return Response('Verification email has been sent', status=status.HTTP_200_OK)
        return Response('Email is already activated', status=status.HTTP_400_BAD_REQUEST)
