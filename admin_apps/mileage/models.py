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

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.user)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.user))
        super(Staff, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mileage:profile', kwargs={'pk': self.pk})

    def get_approve_url(self):
        return reverse('mileage:approve', kwargs={'pk': self.pk})

    def get_pay_url(self):
        return reverse('mileage:pay', kwargs={'pk': self.pk})

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
    staff = models.ForeignKey(Staff)
    trip_begin = models.IntegerField(blank=False)
    trip_end = models.IntegerField(default=0)
    description = models.TextField(blank=False)
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
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

    def get_approve_url(self):
        pass
    def get_delete_url(self):
        pass
    def get_paid_url(self):
        pass

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)