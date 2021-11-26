from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import JobSeeker, Employer

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('is_employer', 'is_job_seeker', 'email_verified')
    list_filter = BaseUserAdmin.list_filter + ('is_employer', 'is_job_seeker')
    list_editable = ('is_staff', 'is_employer', 'is_job_seeker', 'email_verified')


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user',)
