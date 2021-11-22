from django.contrib import admin

from job.models import Job


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SkillInline(admin.TabularInline):
    model = Job.required_skills.through
    extra = 0


class JobAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_filter = ('category__name', 'city__name', 'cooperation_type', 'remote_available', 'sex')
    search_fields = ('title', 'category__name', 'description')
    inlines = [SkillInline]
