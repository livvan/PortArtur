from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/', include('staticpages.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^bus/', include('bus.urls', namespace='bus')),
    url(r'^messages/', include('messages.urls', namespace='messages')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^rpg/', include('rpg.urls', namespace='rpg')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^reports$', TemplateView.as_view(template_name='reports.html'), name='reports'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
