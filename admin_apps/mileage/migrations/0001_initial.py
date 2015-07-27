# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reimbursement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('department', models.CharField(max_length=25)),
                ('payperiod', models.CharField(max_length=25)),
                ('staff', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('trip_begin', models.IntegerField()),
                ('trip_end', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('amount_owed', models.DecimalField(max_digits=10, decimal_places=2)),
                ('distance', models.IntegerField(default=False, blank=True)),
                ('reimbursement', models.ForeignKey(to='mileage.Reimbursement')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
