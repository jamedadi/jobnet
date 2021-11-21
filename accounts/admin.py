from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import JobSeeker, Employer

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'date_joined', 'is_staff', 'is_active', 'user_type')
    list_display_links = ('id', 'username', 'email')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    pass


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass
