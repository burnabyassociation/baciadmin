# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_begin',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_end',
            field=models.IntegerField(),
        ),
    ]
