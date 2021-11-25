from django.db import models

from accounts.models import JobSeeker, Employer
from address.models import City
from company.models import Company
from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _

from resume.models import Resume


class JobCategory(BaseModel):
    name = models.CharField(max_length=48, verbose_name=_('name'), unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('job category')
        verbose_name_plural = _('job categories')
        db_table = 'job_category'


class Skill(BaseModel):
    title = models.CharField(max_length=48, verbose_name=_('name'), unique=True)

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

    MALE = 1
    FEMALE = 2
    SEX_CHOICES = (
        (NOT_IMPORTANT, 'not important'),
        (MALE, _('male')),
        (FEMALE, _('female'))
    )

    Associate = 1
    Bachelor = 2
    DEGREE_CHOICES = (
        (NOT_IMPORTANT, _('not important')),
        (Associate, _('associate')),
        (Bachelor, _('bachelor'))
    )

    SERVED_OR_EXEMPT = 1
    MILITARY_SERVICE_CHOICES = (
        (NOT_IMPORTANT, _('not important')),
        (SERVED_OR_EXEMPT, _('served or exempt'))
    )
    employer = models.ForeignKey(to=Employer, verbose_name=_('employer'), related_name='jobs', on_delete=models.CASCADE)
    company = models.ForeignKey(to=Company, verbose_name=_('company'), related_name='jobs', on_delete=models.CASCADE)

    title = models.CharField(max_length=48, verbose_name=_('name'))
    category = models.ForeignKey(to=JobCategory, verbose_name=_('category'), related_name='jobs',
                                 on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(to=City, verbose_name=_('city'), related_name='jobs', on_delete=models.CASCADE)
    cooperation_type = models.PositiveSmallIntegerField(verbose_name=_('cooperation type'), choices=COOPERATION_CHOICES)
    remote_available = models.BooleanField(verbose_name=_('remote available'), default=False)
    work_experience = models.PositiveSmallIntegerField(verbose_name=_('work experience'),
                                                       choices=WORK_EXPERIENCE_CHOICES, default=0)
    salary_agreement = models.BooleanField(verbose_name=_('salary agreement'), default=True)
    salary = models.PositiveIntegerField(verbose_name=_('salary'), null=True)
    description = models.TextField(verbose_name=_('description'))
    sex = models.PositiveSmallIntegerField(verbose_name=_('sex'), choices=SEX_CHOICES)
    at_least_degree = models.PositiveSmallIntegerField(verbose_name=_('at least degree'), choices=DEGREE_CHOICES)
    required_skills = models.ManyToManyField(to=Skill, verbose_name=_('required skills'), related_name='jobs')
    military_service_status = models.PositiveSmallIntegerField(_('military service status'),
                                                               choices=MILITARY_SERVICE_CHOICES)

    def __str__(self):
        return f"{self.title} ({self.company.name})"

    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        db_table = 'jobs'


class JobRequest(BaseModel):
    NOT_SEEN = 0
    SEEN = 1
    SEEN_STATUS_CHOICES = (
        (SEEN, _('seen')),
        (NOT_SEEN, _('not seen'))
    )

    WAITING = 0
    DENIED = 1
    STATUS_CHOICES = (
        (WAITING, _('waiting')),
        (DENIED, _('denied'))
    )

    job = models.ForeignKey(to=Job, verbose_name=_('job'), related_name='job_requests', on_delete=models.PROTECT)
    job_seeker = models.ForeignKey(to=JobSeeker, verbose_name=_('job seeker'), related_name='job_requests',
                                   on_delete=models.PROTECT)
    resume = models.ForeignKey(to=Resume, verbose_name=_('resume'), related_name='job_requests',
                               on_delete=models.SET_NULL, null=True)
    seen_status = models.PositiveSmallIntegerField(verbose_name=_('seen status'), choices=SEEN_STATUS_CHOICES,
                                                   default=NOT_SEEN)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS_CHOICES, default=WAITING)

    def __str__(self):
        return f"{self.job_seeker} - {self.job}"

    class Meta:
        verbose_name = _('job request')
        verbose_name_plural = _('job requests')
        db_table = 'job_request'
