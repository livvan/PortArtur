# coding: utf8
from __future__ import unicode_literals

from django import forms

from messages import models


ComposeForm = forms.modelform_factory(models.Message, fields=('receiver', 'message'))
TalkForm = forms.modelform_factory(models.Message, fields=('message',))
