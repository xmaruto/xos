# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VRouterService',
            fields=[
            ],
            options={
                'verbose_name': 'vRouter Service',
                'proxy': True,
            },
            bases=('core.service',),
        ),
        migrations.CreateModel(
            name='VRouterTenant',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('core.tenant',),
        ),
    ]
