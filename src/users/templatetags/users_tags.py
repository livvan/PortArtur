# encoding: utf-8
from __future__ import unicode_literals

from django import template

from users import models

register = template.Library()


@register.filter
def nick(user):
    try:
        return models.Profile.objects.get(user=user).nick or u'??'
    except models.Profile.DoesNotExist:
        return '??'
