from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from bus import views

admin.autodiscover()

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url('^report', views.ReportView.as_view(), name='report'),
]
