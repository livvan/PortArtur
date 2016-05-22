# coding: utf8
from __future__ import unicode_literals
from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, FormView, UpdateView, CreateView

from rpg import forms
from rpg import models
from rpg.decorators import class_view_decorator, superuser_required, profile_required, no_role_required


@class_view_decorator(login_required)
@class_view_decorator(profile_required)
@class_view_decorator(no_role_required)
class RequestView(FormView):
    """Выбор роли"""
    template_name = 'rpg/request.html'
    form_class = forms.RequestForm
    success_url = '/'

    def form_valid(self, form):
        form.save(self.request.user)
        return super(RequestView, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(profile_required)
@class_view_decorator(no_role_required)
class RequestNewView(CreateView):
    """Создание роли"""
    template_name = 'rpg/request_new.html'
    form_class = forms.RoleForm
    success_url = '/'

    def form_valid(self, form):
        role = form.save(commit=False)
        role.user = self.request.user
        role.save()
        return super(RequestNewView, self).form_valid(form)


class RolesView(ListView):
    queryset = models.Role.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super(RolesView, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        context['occupied'] = self.queryset.filter(user__isnull=False).count()
        return context


@class_view_decorator(login_required)
class RoleEditView(UpdateView):
    """Редактирование роли"""
    template_name = 'rpg/role_edit.html'
    form_class = forms.RoleForm
    object = None
    queryset = models.Role.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(models.Role, pk=kwargs['pk'])

        if request.user.is_superuser or request.user == self.object.user:
            return super(RoleEditView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get(self, request, *args, **kwargs):
        if self.object.is_locked:
            form = None
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form, role=self.object))

    def post(self, request, *args, **kwargs):
        if self.object.is_locked:
            raise Http404

        return super(RoleEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('role', args=[self.object.pk])


@class_view_decorator(login_required)
class RoleRelationsView(TemplateView):
    """Редактирование связей роли"""
    template_name = 'rpg/role_relations_edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(models.Role, pk=kwargs['pk'])

        if request.user.is_superuser or request.user == self.object.user:
            return super(RoleRelationsView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get(self, request, *args, **kwargs):
        context = {
            'formset': forms.ConnectionFormSet(instance=self.object),
            'object': self.object,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {
            'formset': forms.ConnectionFormSet(request.POST, instance=self.object),
            'object': self.object,
        }

        if context['formset'].is_valid():
            context['formset'].save()
            return HttpResponseRedirect(reverse('role_relations', args=[self.object.id]) + '?save=ok')
        else:
            return self.render_to_response(context)


@class_view_decorator(superuser_required)
class OverviewReport(TemplateView):
    template_name = 'rpg/reports/overview.html'

    def get_context_data(self, **kwargs):
        context = super(OverviewReport, self).get_context_data(**kwargs)

        users = get_user_model().objects.all()
        for user in users:
            if models.UserInfo.objects.filter(user=user).count():
                user.userinfo = models.UserInfo.objects.get(user=user)
            if models.Role.objects.filter(user=user).count():
                user.role = models.Role.objects.get(user=user)
        context['users'] = users
        return context


@class_view_decorator(superuser_required)
class ReportConnectionsDiagram(TemplateView):
    template_name = 'rpg/reports/connections_diagram.html'


@class_view_decorator(superuser_required)
class ReportConnectionsData(TemplateView):
    template_name = 'rpg/reports/connections_diagram.html'

    def get(self, request, **kwargs):
        roles = models.Role.objects.all().order_by('name')
        result = []

        for role in roles:
            result.append({
                'name': str(role.pk),
                'full_name': role.name,
                'link': role.get_absolute_url(),
                'imports': [
                    str(connection.role_rel.pk)
                    for connection in models.RoleConnection.objects.filter(role=role, role_rel__isnull=False)
                ]
            })

        return HttpResponse(dumps(result, indent=2, ensure_ascii=False), content_type='application/json; charset=UTF-8')


@class_view_decorator(superuser_required)
class MoneyReport(TemplateView):
    template_name = 'rpg/reports/money.html'

    def get_context_data(self, **kwargs):
        context = super(MoneyReport, self).get_context_data(**kwargs)
        context['users'] = get_user_model().objects.filter(role__isnull=False).order_by('last_name')
        context['total'] = {
            'payment': 0,
            'cost': 0,
            'debt': 0,
        }
        for user in context['users']:
            user.userinfo, _ = models.UserInfo.objects.get_or_create(user=user)
            user.userinfo.debt = user.userinfo.cost - user.userinfo.payment

            context['total']['cost'] += user.userinfo.cost
            context['total']['payment'] += user.userinfo.payment
            context['total']['debt'] += user.userinfo.debt

        return context


@class_view_decorator(superuser_required)
class BusReport(TemplateView):
    template_name = 'rpg/reports/bus.html'

    def get_context_data(self, **kwargs):
        context = super(BusReport, self).get_context_data(**kwargs)
        context['users'] = get_user_model().objects.filter(role__isnull=False).order_by('last_name')
        context['total'] = 0
        context['total_back'] = 0
        for user in context['users']:
            user.userinfo, _ = models.UserInfo.objects.get_or_create(user=user)

            context['total'] += int(user.userinfo.bus)
            context['total_back'] += int(user.userinfo.bus_back)
        return context


@class_view_decorator(superuser_required)
class FullReport(TemplateView):
    template_name = 'rpg/reports/full.html'

    def get_context_data(self, **kwargs):
        context = super(FullReport, self).get_context_data(**kwargs)
        roles = models.Role.objects.all()
        if self.request.GET.get('n'):
            roles = roles[:int(self.request.GET.get('n'))]
        if self.request.GET.get('id'):
            roles = roles.filter(pk=int(self.request.GET.get('id')))
        context['roles'] = roles
        return context
