# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0009_auto_20150527_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='amount_owed',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
