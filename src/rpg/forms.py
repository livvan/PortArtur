# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.forms.models import modelform_factory

from rpg.models import Role, RoleConnection


class CabinetForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    family = forms.CharField(label='Фамилия', max_length=50)
    nick = forms.CharField(label='Ник', max_length=50)
    age = forms.IntegerField(label='Возраст')
    phone = forms.CharField(label='Телефон', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    city = forms.CharField(label='Город', max_length=50)
    med = forms.CharField(label='Медицина', widget=forms.Textarea,
                          help_text='ваши медицинские особенности, которые надо знать организаторам.')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.userinfo = UserInfo.objects.get(user=user)
        super(CabinetForm, self).__init__(*args, **kwargs)

        self.initial['name'] = user.first_name
        self.initial['family'] = user.last_name
        self.initial['email'] = user.email
        self.initial['nick'] = self.userinfo.nick
        self.initial['age'] = self.userinfo.age
        self.initial['phone'] = self.userinfo.phone
        self.initial['city'] = self.userinfo.city
        self.initial['med'] = self.userinfo.med

    def save(self):
        self.user.first_name = self.cleaned_data['name']
        self.user.last_name = self.cleaned_data['family']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        self.userinfo.nick = self.cleaned_data['nick']
        self.userinfo.age = self.cleaned_data['age']
        self.userinfo.phone = self.cleaned_data['phone']
        self.userinfo.city = self.cleaned_data['city']
        self.userinfo.med = self.cleaned_data['med']
        self.userinfo.save()


class BusForm(forms.Form):
    bus = forms.BooleanField(label='Автобус на базу', required=False)
    bus_back = forms.BooleanField(label='Автобус с базы', required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.userinfo = UserInfo.objects.get(user=user)
        super(BusForm, self).__init__(*args, **kwargs)

        self.initial['bus'] = self.userinfo.bus
        self.initial['bus_back'] = self.userinfo.bus_back

    def save(self):
        self.userinfo.bus = self.cleaned_data['bus']
        self.userinfo.bus_back = self.cleaned_data['bus_back']
        self.userinfo.save()


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

RoleForm = modelform_factory(Role, exclude=('user', 'is_locked'))
ConnectionFormSet = forms.inlineformset_factory(Role, RoleConnection, fk_name='role', exclude=('is_locked',), extra=1)
