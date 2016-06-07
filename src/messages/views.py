# coding: utf8
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView

from rpg.decorators import class_view_decorator, role_required
from rpg.models import Role
from messages import models, forms


@class_view_decorator(role_required)
class IndexView(TemplateView):
    template_name = 'messages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # TODO: сделать на агрегации
        conversation = {}
        for message in models.Message.objects.filter(Q(sender=self.request.role) | Q(receiver=self.request.role)):
            for role in (message.sender, message.receiver):
                if role != self.request.role:
                    name = unicode(role)
                    if name not in conversation:
                        conversation[name] = {'total': 0, 'unread': 0, 'role': role}
                    conversation[name]['total'] += 1
                    if self.request.role == message.receiver and not message.readed:
                        conversation[name]['unread'] += 1

        context['conversation'] = conversation.values()
        context['conversation'].sort(key=lambda t: unicode(t['role']))
        return context


@class_view_decorator(role_required)
class ComposeView(CreateView):
    model = models.Message
    template_name = 'messages/compose.html'
    form_class = forms.ComposeForm

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.role
        message.save()

        message.receiver.send_mail(
            subject='Новое сообщение в личной переписке',
            message='Новое сообщение от %s (%s%s)' %
                    (message.sender, settings.DOMAIN, reverse('messages:talk', args=[message.sender_id]))
        )
        return HttpResponseRedirect(reverse('messages:talk', args=[message.receiver_id]))


@class_view_decorator(role_required)
class TalkView(CreateView):
    model = models.Message
    template_name = 'messages/talk.html'
    form_class = forms.TalkForm

    def dispatch(self, request, *args, **kwargs):
        self.receiver = Role.objects.get(pk=kwargs['pk'])
        return super(TalkView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TalkView, self).get_context_data(**kwargs)
        context['receiver'] = self.receiver
        context['messages'] = models.Message.objects.filter(
            Q(sender=self.request.role, receiver=self.receiver) |
            Q(sender=self.receiver, receiver=self.request.role)
        )
        models.Message.objects.filter(
            Q(receiver=self.request.role, sender=self.receiver)
        ).update(readed=True)
        return context

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.role
        message.receiver = self.receiver
        message.save()

        message.receiver.send_mail(
            subject='Новое сообщение в личной переписке',
            message='Новое сообщение от %s (%s%s)' %
                    (message.sender, settings.DOMAIN, reverse('messages:talk', args=[message.sender_id]))
        )
        return HttpResponseRedirect(reverse('messages:talk', args=[message.receiver_id]))
