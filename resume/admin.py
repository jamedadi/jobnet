from django.contrib import admin

from resume.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'file')
    search_fields = ('job_seeker__username',)
