# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0003_auto_20150727_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trip_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 21, 40, 9, 106228, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
