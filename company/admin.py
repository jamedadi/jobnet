from django.contrib import admin

from company.models import CompanyType, Company, EmployeeType, Employee


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('persian_name', 'english_name', 'foundation', 'site', 'logo', 'banner', 'type')
    list_filter = ('type',)


@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
