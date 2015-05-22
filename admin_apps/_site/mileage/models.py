# mileage.models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Payperiod(TimeStampedModel):

    due = models.DateTimeField(blank=False)


    def __unicode__(self):
        return self.date
        
    @classmethod
    def get_next_pay_period(self):
        p = Payperiod.objects.all().order_by('-due')[0]
        Payperiod.objects.all().order_by('-due')[0].delete()
        return p

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

    def __unicode__(self):
        return self.description

    def get_amount_owed(self):
        total_kms = self.trip_end - self.trip_begin
        return total_kms*(0.45)

    def get_amount_owed_string(self):
        total_kms = self.trip.end - self.trip_begin
        return str(total_kms*(0.45))

    def get_absolute_url(self):
        return reverse('mileage:detail', kwargs={'pk': self.id})