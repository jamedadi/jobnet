from rest_framework import serializers

from company.models import Company, CompanyType, EmployeeType


class CompanySerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Company
        exclude = ('employer', 'modified_time')


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ('id', 'type',)
        read_only_fields = ('id',)


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = ('id', 'type',)
        read_only_fields = ('id',)
