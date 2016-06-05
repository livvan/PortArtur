# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.forms.models import modelform_factory

from rpg.models import Role, RoleConnection


class RequestForm(forms.Form):
    role = forms.IntegerField(label='Роль', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        self.fields['role'].widget.choices = [
            (role.id, role.name)
            for role in Role.objects.filter(user__isnull=True)
        ]

    def clean_role(self):
        try:
            return Role.objects.get(pk=self.cleaned_data['role'], user__isnull=True)
        except Role.DoesNotExist:
            raise forms.ValidationError('Неизвестная роль')

    def save(self, user):
        self.cleaned_data['role'].user = user
        self.cleaned_data['role'].save()

        user.role = self.cleaned_data['role']
        user.save()

RoleForm = modelform_factory(Role, exclude=('user',))
ConnectionFormSet = forms.inlineformset_factory(Role, RoleConnection, fk_name='role', exclude=('is_locked',), extra=1)
