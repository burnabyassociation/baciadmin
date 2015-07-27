# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0002_auto_20150727_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
