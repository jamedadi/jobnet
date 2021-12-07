from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from rest_framework import mixins
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response

from accounts.api.permissions import IsNotAuthenticated, IsJobSeeker, IsEmployer
from accounts.api.serializers import UserRegistrationSerializer, UserChangePasswordSerializer, \
    JobSeekerSerializer, EmployerSerializer, UserInfoSerializer, CustomTokenObtainPairSerializer, EmailSerializer, \
    ResetPasswordSerializer
from accounts.models import JobSeeker, Employer
from accounts.tasks import send_email_task

User = get_user_model()


class UserRegistrationCreateApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'employer':
            user = serializer.save(is_employer=True)
            send_email_task.delay(user.pk, 'email_verification')
        elif user_type == 'job-seeker':
            user = serializer.save(is_job_seeker=True)
            send_email_task.delay(user.pk, 'email_verification')
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

    def get(self, request, uib64, token, *args, **kwargs):
        try:
            user_id = smart_str(urlsafe_base64_decode(uib64))
        except DjangoUnicodeDecodeError:
            return Response('can\'t decode url', status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        else:
            if not default_token_generator.check_token(user, token):
                return Response('Token is invalid or expired.', status=status.HTTP_400_BAD_REQUEST)
            user.email_verified = True
            user.save()
            return Response('Email successfully confirmed')


class ResendEmail(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User with this email has not been found', status=status.HTTP_404_NOT_FOUND)
        else:
            if not user.email_verified:
                send_email_task.delay(user.pk, 'email_verification')
                return Response('Verification email has been sent', status=status.HTTP_200_OK)
            return Response('Email is already activated', status=status.HTTP_400_BAD_REQUEST)


class RequestResetEmailPasswordAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User with this email has not been found', status=status.HTTP_404_NOT_FOUND)
        else:
            send_email_task.delay(user.pk, 'reset_password')
            return Response('Verification email has been sent', status=status.HTTP_200_OK)


class ResetEmailPasswordAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = ResetPasswordSerializer

    def patch(self, request, uib64, token, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = smart_str(urlsafe_base64_decode(uib64))
        except DjangoUnicodeDecodeError:
            return Response('can\'t decode url', status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        else:
            if not default_token_generator.check_token(user, token):
                return Response('Token is invalid or expired.', status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()

            return Response('password changed successfully', status=status.HTTP_200_OK)
