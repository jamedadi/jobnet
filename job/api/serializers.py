from rest_framework import serializers

from job.models import JobCategory, Skill, Job


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('id', 'name')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'title')


class ReadJobSerializer(serializers.ModelSerializer):
    def get_company(self, obj):
        return {
            'id': obj.company.id,
            'name': obj.company.name
        }

    def get_city(self, obj):
        return {
            'state': obj.city.state.name,
            'city': obj.city.name
        }

    company = serializers.SerializerMethodField('get_company')
    category = serializers.CharField(source='category.name')
    city = serializers.SerializerMethodField('get_city')
    cooperation_type = serializers.CharField(source='get_cooperation_type_display')
    work_experience = serializers.CharField(source='get_work_experience_display')
    sex = serializers.CharField(source='get_sex_display')
    at_least_degree = serializers.CharField(source='get_at_least_degree_display')
    required_skills = serializers.StringRelatedField(many=True)
    military_service_status = serializers.CharField(source='get_military_service_status_display')

    class Meta:
        model = Job
        exclude = ('employer',)


class WriteJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('employer', 'company', 'created_time', 'modified_time')
