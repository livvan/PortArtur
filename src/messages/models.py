# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from rpg.models import Role


class Message(models.Model):
    sender = models.ForeignKey(Role, verbose_name='Роль', related_name='sended')
    receiver = models.ForeignKey(Role, verbose_name='Роль', related_name='received')
    message = models.TextField(verbose_name='Сообщение')
    readed = models.BooleanField(verbose_name='Прочитано', default=False)
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-id',)
