# coding: utf8
from __future__ import unicode_literals
import uuid

from django import forms
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from users import models


class CabinetForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    family = forms.CharField(label='Фамилия', max_length=50)
    nick = forms.CharField(label='Ник', max_length=50)
    age = forms.IntegerField(label='Возраст')
    phone = forms.CharField(label='Телефон', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    city = forms.CharField(label='Город', max_length=50)
    med = forms.CharField(
        label='Медицина', widget=forms.Textarea, required=False,
        help_text='Хронические заболевания, которые могут обостриться на игре / медицинские противопоказания.',
    )
    wishes = forms.CharField(
        label='Пожелания', widget=forms.Textarea, required=False,
        help_text='Во что вы хотите играть. Подробно и по пунктам.',
    )
    hates = forms.CharField(
        label='Нежелания', widget=forms.Textarea, required=False,
        help_text='Во что вы категорически не хотите играть. Так же подробно и по пунктам.',
    )

    def __init__(self, user, *args, **kwargs):
        if not user.is_authenticated():
            return

        self.user = user
        self.profile, _ = models.Profile.objects.get_or_create(user=self.user)
        super(CabinetForm, self).__init__(*args, **kwargs)

        self.initial['name'] = self.user.first_name
        self.initial['family'] = self.user.last_name
        self.initial['email'] = self.user.email
        self.initial['nick'] = self.profile.nick
        self.initial['age'] = self.profile.age
        self.initial['phone'] = self.profile.phone
        self.initial['city'] = self.profile.city
        self.initial['med'] = self.profile.med
        self.initial['wishes'] = self.profile.wishes
        self.initial['hates'] = self.profile.hates

    def save(self):
        self.user.first_name = self.cleaned_data['name']
        self.user.last_name = self.cleaned_data['family']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        self.profile.nick = self.cleaned_data['nick']
        self.profile.age = self.cleaned_data['age']
        self.profile.phone = self.cleaned_data['phone']
        self.profile.city = self.cleaned_data['city']
        self.profile.med = self.cleaned_data['med']
        self.profile.wishes = self.cleaned_data['wishes']
        self.profile.hates = self.cleaned_data['hates']
        self.userinfo.save()


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=100)

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Такой email на сайте уже есть. Может, вы регистрировались у нас?')
        return self.cleaned_data['email']

    def save(self):
        password = get_random_string(20, '0123456789abcdefghijklmnopqrstuvwxyz')
        email = self.cleaned_data['email']

        user = get_user_model().objects.create_user(
            username=uuid.uuid4().hex[:30],
            password=password,
            email=email,
        )
        user.is_active = True
        user.save()

        models.Profile.objects.create(user=user)

        auth_user = authenticate(username=user.username, password=password)

        return auth_user, password


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def clean(self):
        if self.errors:
            return

        User = get_user_model()
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError('Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=self.cleaned_data['password'])
        if auth_user:
            self.cleaned_data['user'] = auth_user
            return self.cleaned_data
        else:
            raise forms.ValidationError('Логин или пароль не верен')
