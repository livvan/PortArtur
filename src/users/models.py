# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from yafotki.fields import YFField

ALBUM = getattr(settings, 'YAFOTKI_ALBUM', 'default')


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None)
    nick = models.CharField(verbose_name='Ник', blank=True, default='', max_length=255)
    phone = models.CharField(blank=True, default='', max_length=255)
    city = models.CharField(blank=True, default='', max_length=255)
    age = models.IntegerField(verbose_name='Возраст', blank=True, null=True, default=None)
    med = models.TextField(verbose_name='Медицина', default='', blank=True)
    photo = YFField(verbose_name='Фото', upload_to=ALBUM, blank=True, null=True, default=None)
    wishes = models.TextField(verbose_name='Во что хотите играть', default='', blank=True)
    hates = models.TextField(verbose_name='Во что не хотите играть', default='', blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
