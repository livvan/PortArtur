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

    def save(self, *args, **kwargs):
        if not self.id:
            self.sender.records.create(
                category='Переписка',
                message='Вы отправили сообщение для %s' % self.receiver.name
            )
            self.receiver.records.create(
                category='Переписка',
                message='Вы получили сообщение от %s' % self.sender.name
            )
        return super(Message, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-id',)
