from rest_framework import serializers

from resume.models import Resume


class ResumeSerializers(serializers.ModelSerializer):

    def get_job_seeker(self, obj):
        return {
            'id': obj.job_seeker.user.id,
            'full name': obj.job_seeker.user.get_full_name(),
            'username': obj.job_seeker.user.username,
            'email': obj.job_seeker.user.email,
        }

    job_seeker = serializers.SerializerMethodField('get_job_seeker')

    class Meta:
        model = Resume
        fields = ('id', 'file', 'job_seeker')
