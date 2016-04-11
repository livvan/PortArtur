# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from jsonfield.fields import JSONField

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Bus(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, verbose_name='Человек')
    bus = JSONField(verbose_name='Автобус', default=None)

    class Meta:
        verbose_name = 'Автобус'
        verbose_name_plural = 'Автобус'
