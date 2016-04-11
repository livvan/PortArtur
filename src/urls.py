from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^articles/', include('staticpages.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^bus/', include('bus.urls', namespace='bus')),
    url(r'^messages/', include('messages.urls', namespace='messages')),
    url(r'^', include('rpg.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
