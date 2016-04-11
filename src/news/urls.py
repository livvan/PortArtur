from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import ListView
from news import models

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=models.News.objects.all()), name='news'),
]
