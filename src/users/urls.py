# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^cabinet$', views.CabinetView.as_view(), name='cabinet'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^registration', views.RegistrationView.as_view(), name='registration'),
]
