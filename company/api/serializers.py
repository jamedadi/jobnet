from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Company
        exclude = ('employer', 'modified_time')
