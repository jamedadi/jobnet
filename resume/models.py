from django.db import models

from accounts.models import JobSeeker
from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Resume(BaseModel):
    job_seeker = models.ForeignKey(to=JobSeeker, verbose_name=_('job seeker'), related_name='resumes',
                                   on_delete=models.CASCADE)
    file = models.FileField(verbose_name=_('file'), upload_to='resumes/')

    def __str__(self):
        return self.file.url

    class Meta:
        verbose_name = _('resume')
        verbose_name_plural = _('resumes')
        db_table = 'resume'
