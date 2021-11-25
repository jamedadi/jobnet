from django.db import models
from django.utils.text import slugify

from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class State(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'), unique=True)
    slug = models.SlugField(verbose_name=_('slug'), unique=True, allow_unicode=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')
        db_table = 'state'


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'), unique=True, allow_unicode=True, null=True)
    state = models.ForeignKey(to=State, verbose_name=_('state'), related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        db_table = 'city'
