# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0006_trip_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payperiod',
            name='due',
            field=models.DateField(),
        ),
    ]
