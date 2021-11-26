from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.postgres.fields import CICharField

from django.utils.translation import ugettext_lazy as _
from django.db import models

from lib.models import BaseModel


class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = CICharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(_('email verified'), default=False)
    phone_number = models.CharField(max_length=9, verbose_name=_('phone number'), blank=True)
    is_employer = models.BooleanField(default=False, verbose_name=_('is employer'))
    is_job_seeker = models.BooleanField(default=False, verbose_name=_('is job seeker'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'


class Employer(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT, primary_key=True, verbose_name=_('user'),
                                related_name='employer')

    class Meta:
        verbose_name = _('employer')
        verbose_name_plural = _('employers')
        db_table = 'employer'

    def __str__(self):
        return f"{self.user.username}"


class JobSeeker(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT, primary_key=True, verbose_name=_('user'),
                                related_name='job_seeker')
    birthday = models.DateField(verbose_name=_('birthday'), blank=True, null=True)

    class Meta:
        verbose_name = _('job seeker')
        verbose_name_plural = _('job seekers')
        db_table = 'job_seeker'
