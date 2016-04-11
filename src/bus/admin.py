from __future__ import unicode_literals

from django.contrib import admin
from bus import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('user',)
    raw_id_fields = ('user',)
