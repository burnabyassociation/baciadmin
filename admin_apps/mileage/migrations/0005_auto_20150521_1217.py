# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0004_auto_20150521_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payperiod',
            name='user',
        ),
        migrations.AlterField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
