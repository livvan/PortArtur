# coding: utf-8
from __future__ import unicode_literals
from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

admin.site.register(Article, ArticleAdmin)
