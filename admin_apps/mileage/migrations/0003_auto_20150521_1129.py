# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0002_auto_20150515_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payperiod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('due', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_end',
            field=models.IntegerField(default=0),
        ),
    ]
