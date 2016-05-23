# coding: utf-8
from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

from ..models import Article

register = template.Library()


@register.simple_tag()
def content(article_id):
    try:
        if isinstance(article_id, int) or article_id.isdigit():
            return mark_safe(Article.objects.get(pk=article_id).content)
        else:
            return mark_safe(Article.objects.get(title=article_id).content)

    except Article.DoesNotExist:
        return ''
