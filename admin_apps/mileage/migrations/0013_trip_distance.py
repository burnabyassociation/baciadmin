# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0012_remove_trip_total_amount_owed'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='distance',
            field=models.IntegerField(default=False, blank=True),
        ),
    ]
