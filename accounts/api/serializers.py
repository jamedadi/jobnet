from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from accounts.models import JobSeeker, Employer

User = get_user_model()


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
