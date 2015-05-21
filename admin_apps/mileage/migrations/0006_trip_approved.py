# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0005_auto_20150521_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
