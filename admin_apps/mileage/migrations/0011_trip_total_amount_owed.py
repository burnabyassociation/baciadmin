# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0010_trip_amount_owed'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='total_amount_owed',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
