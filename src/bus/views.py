# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView, TemplateView

from bus import models, forms
from rpg.decorators import class_view_decorator, role_required, superuser_required


@class_view_decorator(role_required)
class IndexView(FormView):
    template_name = 'bus/index.html'
    form_class = forms.BusForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['saved'] = self.request.GET.get('save')
        return context

    def get_form_kwargs(self):
        kwargs = super(IndexView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('bus:index') + '?save=ok')


@class_view_decorator(superuser_required)
class ReportView(TemplateView):
    template_name = 'bus/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()
        requests = list(models.Bus.objects.all().order_by('user__last_name'))
        context['tables'] = []

        for n, variant in enumerate(settings.BUS_VARIANTS):
            context['tables'].append({
                'title': variant,
                'users': [request.user for request in requests if request.bus[n]],
            })

        return context
