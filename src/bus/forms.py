# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from bus import models


class BusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BusForm, self).__init__(*args, **kwargs)

        self.bus, _ = models.Bus.objects.get_or_create(
            user=self.user, defaults={'bus': [False] * len(settings.BUS_VARIANTS)}
        )

        for n, variant in enumerate(settings.BUS_VARIANTS):
            self.fields['bus%s' % n] = forms.BooleanField(label=variant, required=False, initial=self.bus.bus[n])

    def save(self):
        for n, variant in enumerate(settings.BUS_VARIANTS):
            self.bus.bus[n] = self.cleaned_data['bus%s' % n]
        self.bus.save()
