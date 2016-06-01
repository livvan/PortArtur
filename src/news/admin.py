# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from news import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('content',)
    actions = ['notify']

    def notify(self, request, queryset):
        for news in queryset.all():
            for user in User.objects.all():
                if user.email:
                    send_html_mail(
                        'ПортАртур: новость на сайте',
                        news.content,
                        [user.email]
                    )
    notify.short_description = 'Отправить письма'


def send_html_mail(subject, message, recipient_list):
    try:
        if not isinstance(recipient_list, list):
            recipient_list = [recipient_list]
        message = EmailMessage(subject, message, to=recipient_list)
        message.content_subtype = 'html'
        message.send()

    except Exception:
        pass
