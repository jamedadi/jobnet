from rest_framework import serializers

from job.models import JobCategory, Skill, Job


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('name',)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('title',)


class ReadJobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Job
        fields = '__all__'
