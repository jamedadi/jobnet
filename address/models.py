from django.db import models

from lib.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class State(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        db_table = 'state'


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    state = models.ForeignKey(to=State, verbose_name=_('state'), related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'
