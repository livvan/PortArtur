# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-31 09:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import yafotki.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(blank=True, default='', max_length=255, verbose_name='\u041d\u0438\u043a')),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=255)),
                ('age', models.IntegerField(blank=True, default=None, null=True, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442')),
                ('med', models.TextField(blank=True, default='', verbose_name='\u041c\u0435\u0434\u0438\u0446\u0438\u043d\u0430')),
                ('photo', yafotki.fields.YFField(blank=True, default=None, max_length=255, null=True, upload_to='default', verbose_name='\u0424\u043e\u0442\u043e')),
                ('wishes', models.TextField(blank=True, default='', verbose_name='\u0412\u043e \u0447\u0442\u043e \u0445\u043e\u0442\u0438\u0442\u0435 \u0438\u0433\u0440\u0430\u0442\u044c')),
                ('hates', models.TextField(blank=True, default='', verbose_name='\u0412\u043e \u0447\u0442\u043e \u043d\u0435 \u0445\u043e\u0442\u0438\u0442\u0435 \u0438\u0433\u0440\u0430\u0442\u044c')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u0444\u0438\u043b\u044c',
                'verbose_name_plural': '\u041f\u0440\u043e\u0444\u0438\u043b\u0438',
            },
        ),
    ]
