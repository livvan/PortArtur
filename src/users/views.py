# coding: utf8
from __future__ import unicode_literals

from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.core.mail import send_mail

from users import forms


class CabinetView(FormView):
    """Редактирование профиля"""
    template_name = 'users/profile_edit.html'
    form_class = forms.CabinetForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('users:login'))
        return super(CabinetView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CabinetView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CabinetView, self).form_valid(form)


class RegistrationView(FormView):
    """регистрация на сайте"""
    template_name = 'users/registration.html'
    form_class = forms.RegistrationForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('users:cabinet'))
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user, password = form.save()

        login(self.request, user)

        send_mail(
            'Регистрация на сайте ПортАртур',
            'Вы зарегистрировались на сайте http://port-artur.com.ru\nВаш пароль: %s' % password,
            None,
            [user.email],
        )

        return super(RegistrationView, self).form_valid(form)


class LoginView(FormView):
    """Вход на сайт"""
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('users:cabinet'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super(LoginView, self).form_valid(form)
