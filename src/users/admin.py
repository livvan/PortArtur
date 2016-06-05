# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from users import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nick')
    ordering = ('user',)
    raw_id_fields = ('user',)
