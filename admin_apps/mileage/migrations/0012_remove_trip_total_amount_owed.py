# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0011_trip_total_amount_owed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='total_amount_owed',
        ),
    ]
