from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=_('modified time'), auto_now=True)

    class Meta:
        abstract = True
