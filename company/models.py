import khayyam

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import Employer
from address.models import City
from lib.models import BaseModel


def year_choices():
    return [(y, y) for y in range(1280, khayyam.JalaliDatetime.today().year + 1)]


class CompanyType(BaseModel):
    type = models.CharField(max_length=60, verbose_name=_('type'), unique=True)

    class Meta:
        verbose_name = _('company type')
        verbose_name_plural = _('company types')
        db_table = 'company_type'

    def __str__(self):
        return self.type


class Company(BaseModel):
    persian_name = models.CharField(max_length=150, verbose_name=_('persian name'))
    english_name = models.CharField(max_length=150, verbose_name=_('english name'))
    foundation = models.PositiveSmallIntegerField(_('year'), choices=year_choices())
    site = models.URLField(verbose_name=_('site'), blank=True)
    logo = models.ImageField(upload_to='company/logos/', verbose_name=_('logo'), null=True, blank=True)
    banner = models.ImageField(upload_to='company/banners/', verbose_name=_('banner'), null=True, blank=True)
    type = models.ForeignKey(CompanyType, on_delete=models.PROTECT, related_name='companies', verbose_name='type')
    number_of_employees = models.PositiveSmallIntegerField(verbose_name=_('number of employees'))
    description = models.TextField(verbose_name=_('description'))
    city = models.ForeignKey(to=City, verbose_name=_('city'), related_name='companies', on_delete=models.CASCADE)
    introduction = models.TextField(verbose_name=_('introduction'), blank=True)
    culture = models.TextField(verbose_name=_('culture'), blank=True)
    advantage = models.TextField(verbose_name=_('advantage'), blank=True)
    employer = models.OneToOneField(to=Employer, verbose_name=_('employer'), related_name='company',
                                    on_delete=models.CASCADE)

    @property
    def name(self):
        return f"{self.persian_name} | {self.english_name}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        db_table = 'company'


class EmployeeType(BaseModel):
    type = models.CharField(max_length=60, verbose_name=_('type'), unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('type')
        verbose_name_plural = _('types')
        db_table = 'type'


class Employee(BaseModel):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    image = models.ImageField(upload_to='employee/images/', verbose_name=_('image'))
    description = models.TextField(verbose_name=_('description'))
    type = models.ForeignKey(EmployeeType, on_delete=models.PROTECT, related_name='employees', verbose_name=_('type'))
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name=_('company')
    )

    def __str__(self):
        return f"{self.name} | {self.type}"

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        db_table = 'employee'
