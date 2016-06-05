# coding: utf-8
from __future__ import unicode_literals
from django.contrib import admin

from rpg import models


class RoleConnectionInline(admin.TabularInline):
    model = models.RoleConnection
    fk_name = 'role'
    extra = 0


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name')
    inlines = (RoleConnectionInline,)
    list_filter = ('character_1', 'character_2', 'character_3', 'character_4', 'character_5', )


@admin.register(models.RoleConnection)
class RoleConnectionAdmin(admin.ModelAdmin):
    list_display = ('role', 'role_rel')
