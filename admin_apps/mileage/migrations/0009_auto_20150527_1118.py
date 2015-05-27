# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0008_trip_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payperiod',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='trip',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
