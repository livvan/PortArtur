from __future__ import unicode_literals

from django.contrib import admin

from messages import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'dt')
    ordering = ('-id',)
    list_filter = ('sender',)
    search_fields = ('message',)
    raw_id_fields = ('sender', 'receiver')
