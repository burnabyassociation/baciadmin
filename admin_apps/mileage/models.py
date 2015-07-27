# mileage.models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from django.db.models.signals import post_save
from django.utils.text import slugify

import datetime


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(default=datetime.datetime.now, editable=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Reimbursement(TimeStampedModel):

    staff = models.ForeignKey(User)
    department = models.CharField(max_length=25, blank=False)
    payperiod = models.CharField(max_length=25, blank=False)

    def __unicode__(self):
        return self.payperiod

    def get_absolute_url(self):
        return reverse('mileage:detail_reimbursement', kwargs={'pk': self.id})

class Trip(TimeStampedModel):
    """
    Staff will track a trip by it's odometer. They will record the beginning
    and the end of the odometer.
    """
    reimbursement = models.ForeignKey(Reimbursement)
    trip_begin = models.IntegerField(blank=False)
    trip_end = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=False)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    distance = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.amount_owed = (self.trip_end - self.trip_begin)*0.45
        self.distance = (self.trip_end - self.trip_begin)
        super(Trip, self).save(*args, **kwargs)


    def get_absolute_url(self):
        pass