from django.contrib import admin

from job.models import Job, JobCategory, Skill


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Skill)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class SkillInline(admin.TabularInline):
    model = Job.required_skills.through
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'category', 'city', 'cooperation_type', 'remote_available', 'work_experience',
                    'salary_agreement', 'salary', 'description', 'sex', 'at_least_degree', 'military_service_status')
    list_filter = ('cooperation_type', 'remote_available', 'sex')
    search_fields = ('title', 'category__name', 'description')
    inlines = [SkillInline]
