# mileage.models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

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

class StaffProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        slugname = self.user.first_name + self.user.last_name
        self.slug = slugify(slugname)
        super(StaffProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mileage:staff', kwargs={'slug': self.slug})

class Payperiod(TimeStampedModel):
    due = models.DateField(blank=False)

    def __unicode__(self):
        return self.due.strftime('%m/%d/%Y')

    def get_absolute_url(self):
        return reverse('mileage:payperiodlist', kwargs={'pk': self.id})
    
    def clean(self):
        if self.due < timezone.now().date():
            raise ValidationError("payperiods have to be in the future")
    

class Trip(TimeStampedModel):
    """
    Staff will track a trip by it's odometer. They will record the beginning
    and the end of the odometer.
    """
    user = models.ForeignKey(User)
    trip_begin = models.IntegerField(blank=False)
    trip_end = models.IntegerField(default=0)
    description = models.TextField(blank=False)
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(blank=True, default='', max_length=30)
    amount_owed = models.IntegerField(blank=True,default=False)
    distance = models.IntegerField(blank=True, default=False)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.amount_owed = (self.trip_end - self.trip_begin)*0.45
        self.distance = (self.trip_end - self.trip_begin)
        super(Trip, self).save(*args, **kwargs)

    def get_amount_owed(self):
        total_kms = self.trip_end - self.trip_begin
        self.amount_owed = total_kms*(0.45)
        return total_kms*(0.45)

    def get_amount_owed_string(self):
        total_kms = self.trip.end - self.trip_begin
        return str(total_kms*(0.45))

    def get_absolute_url(self):
        return reverse('mileage:detail', kwargs={'pk': self.id})