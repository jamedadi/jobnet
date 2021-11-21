from django.db import models

from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Resume(BaseModel):
    # TODO: job_seeker
    file = models.FileField(verbose_name=_('file'))
