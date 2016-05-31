# coding: utf-8
from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import DetailView
from rpg import views, models

urlpatterns = [
    url(r'^request$', views.RequestView.as_view(), name='request'),
    url(r'^request/new$', views.RequestNewView.as_view(), name='request_new'),

    url(r'^roles', views.RolesView.as_view(), name='roles'),
    url(r'^role/(?P<pk>\d+)$', DetailView.as_view(model=models.Role), name='role'),
    url(r'^role/(?P<pk>\d+)/edit$', views.RoleEditView.as_view(), name='role_edit'),
    url(r'^role/(?P<pk>\d+)/relations$', views.RoleRelationsView.as_view(), name='role_relations'),

    url(r'^reports/overview$', views.OverviewReport.as_view(), name='report_overview'),
    url(r'^reports/connections_diagram$', views.ReportConnectionsDiagram.as_view(),
        name='report_connections_diagram'),
    url(r'^reports/connections_diagram.json$', views.ReportConnectionsData.as_view(),
        name='report_connections_json'),
    url(r'^reports/money$', views.MoneyReport.as_view(), name='report_money'),
    url(r'^reports/bus', views.BusReport.as_view(), name='report_bus'),
    url(r'^reports/full$', views.FullReport.as_view(), name='report_full'),
]
