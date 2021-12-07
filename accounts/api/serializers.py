from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.api.exceptions import EmailNotVerified
from accounts.models import JobSeeker, Employer
from accounts.tasks import send_email_task

User = get_user_model()


class BaseUserUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        instance = super().update(instance, validated_data)

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, attrs):
        # here check password is strong or what! :D
        validate_password(attrs.get('password'))

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('Password and Confirm Password isn\'t equal!'))

        return attrs

    @staticmethod
    def clean_validated_data(validated_data):
        validated_data.pop('confirm_password')  # here delete confirm password because we dont need that
        return validated_data

    @staticmethod
    def create_sub_user(user):
        if user.is_employer:
            Employer.objects.create(user=user)
        elif user.is_job_seeker:
            JobSeeker.objects.create(user=user)

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**self.clean_validated_data(validated_data))
        self.create_sub_user(user)
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        # here check password is strong or what! :D
        validate_password(attrs.get('new_password'))

        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('Password and Confirm Password isn\'t equal!'))

        return attrs

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get('old_password')):
            instance.password = make_password(validated_data.get('new_password'))
            instance.save()
            return instance
        raise serializers.ValidationError(_('Old Password and Password isn\'t equal!'))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')


class JobSeekerSerializer(BaseUserUpdateSerializer):
    user = UserSerializer()

    class Meta:
        model = JobSeeker
        fields = ('user', 'birthday')


class EmployerSerializer(BaseUserUpdateSerializer):
    user = UserSerializer()

    class Meta:
        model = Employer
        fields = ('user',)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_employer', 'is_job_seeker')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.email_verified:
            send_email_task.delay(self.user.pk, 'email_verification')
            raise EmailNotVerified

        data.update({'user_id': self.user.id, 'username': self.user.username, 'email': self.user.email})
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        fields = ('new_password', 'confirm_password')

    def validate(self, attrs):
        # here check password is strong or what! :D
        validate_password(attrs.get('new_password'))

        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('Password and Confirm Password isn\'t equal!'))
        return attrs
