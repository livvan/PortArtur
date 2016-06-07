# coding: utf-8
from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def role_link(context):
    if context['request'].role:
        return reverse('rpg:role_edit', args=[context['request'].role.id])
    else:
        return reverse('rpg:request')
