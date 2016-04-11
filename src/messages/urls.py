# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from messages import views

urlpatterns = [
    url(r'^compose$', views.ComposeView.as_view(), name='compose'),
    url(r'^talk/(?P<pk>\d+)$', views.TalkView.as_view(), name='talk'),
    url(r'', views.IndexView.as_view(), name='index'),
]
