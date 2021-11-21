from django.db import models

from address.models import City
from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class JobCategory(BaseModel):
    name = models.CharField(max_length=48, verbose_name=_('name'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('job category')
        verbose_name_plural = _('job categories')
        db_table = 'job_category'


class Skill(BaseModel):
    title = models.CharField(max_length=48, verbose_name=_('name'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('skill')
        verbose_name_plural = _('skills')
        db_table = 'skill'


class Job(BaseModel):
    NOT_IMPORTANT = 0
    LESS_THAN_THREE = 1
    BETWEEN_THREE_AND_SIX = 2
    MORE_THAN_SIX = 3
    WORK_EXPERIENCE_CHOICES = (
        (NOT_IMPORTANT, _('not important')),
        (LESS_THAN_THREE, _('less than three')),
        (BETWEEN_THREE_AND_SIX, _('between three and six')),
        (MORE_THAN_SIX, _('more than six'))
    )

    FULL_TIME = 0
    PART_TIME = 1
    COOPERATION_CHOICES = (
        (FULL_TIME, _('full time')),
        (PART_TIME, _('part time'))
    )

    MALE = 0
    FEMALE = 1
    SEX_CHOICES = (
        (NOT_IMPORTANT, 'not important'),
        (MALE, _('male')),
        (FEMALE, _('female'))
    )

    Associate = 0
    Bachelor = 1
    DEGREE_CHOICES = (
        (NOT_IMPORTANT, _('not important')),
        (Associate, _('associate')),
        (Bachelor, _('bachelor'))
    )

    # TODO : company
    title = models.CharField(max_length=48, verbose_name=_('name'))
    category = models.ForeignKey(to=JobCategory, verbose_name=_('category'), related_name='jobs',
                                 on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(to=City, verbose_name=_('address'), related_name='jobs', on_delete=models.CASCADE)
    cooperation_type = models.PositiveSmallIntegerField(verbose_name=_('cooperation type'), choices=COOPERATION_CHOICES)
    remote_available = models.BooleanField(verbose_name=_('remote available'), default=False)
    work_experience = models.PositiveSmallIntegerField(verbose_name=_('work experience'),
                                                       choices=WORK_EXPERIENCE_CHOICES, default=0)
    salary_agreement = models.BooleanField(verbose_name=_('salary agreement'), default=True)
    salary = models.PositiveIntegerField(verbose_name=_('salary'))
    description = models.TextField(verbose_name=_('description'))
    sex = models.PositiveSmallIntegerField(verbose_name=_('sex'), choices=SEX_CHOICES)
    at_least_degree = models.PositiveSmallIntegerField(verbose_name=_('at least degree'), choices=DEGREE_CHOICES)
    required_skills = models.ManyToManyField(to=Skill, verbose_name=_('required skills'), related_name='jobs')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        db_table = 'jobs'