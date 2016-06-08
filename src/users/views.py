# coding: utf8
from __future__ import unicode_literals

from django.contrib.auth import login, get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail

from rpg.decorators import class_view_decorator, superuser_required
from users import forms
from users.models import Profile


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


@class_view_decorator(superuser_required)
class MoneyReport(TemplateView):
    template_name = 'users/reports/money.html'

    def get_context_data(self, **kwargs):
        context = super(MoneyReport, self).get_context_data(**kwargs)
        context['users'] = get_user_model().objects.filter(role__isnull=False).order_by('last_name')
        context['total'] = {
            'money': 0,
        }
        for user in context['users']:
            user.profile, _ = Profile.objects.get_or_create(user=user)
            context['total']['money'] += user.profile.money

        return context
