# coding: utf-8
from __future__ import unicode_literals
from django.contrib import admin

from rpg import models


class RoleConnectionInline(admin.TabularInline):
    model = models.RoleConnection
    fk_name = 'role'
    extra = 0


class RoleAdmin(admin.ModelAdmin):
    list_display = ('username', 'role_name')
    inlines = (RoleConnectionInline,)


class RoleConnectionAdmin(admin.ModelAdmin):
    list_display = ('role', 'role_rel')


admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.RoleConnection, RoleConnectionAdmin)
