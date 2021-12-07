from rest_framework import serializers

from company.models import Company, CompanyType, EmployeeType, Employee


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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('company', 'modified_time')
        read_only_fields = ('id',)


class CompanySerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(read_only=True)
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        exclude = ('employer', 'modified_time')
        read_only_fields = ('id',)
