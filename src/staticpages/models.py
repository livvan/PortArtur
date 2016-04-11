# coding: utf-8
from __future__ import unicode_literals
from django.db import models

from redactor.fields import RedactorField


class Article(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    content = RedactorField(verbose_name='Содержание')
    url = models.CharField(verbose_name='Ссылка', max_length=255, null=True, blank=True, default=None,
                           help_text='Вместо отображения текста будет переход по ссылке')
    order = models.PositiveSmallIntegerField(verbose_name='Порядок', default=100)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ('order',)
