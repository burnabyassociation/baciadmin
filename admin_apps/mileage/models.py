# mileage.models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    #user = models.ForeignKey(User, default=0)
    due = models.DateField(blank=False)

    def __unicode__(self):
        return self.due.strftime('%m/%d/%Y')

    @classmethod
    def get_current_payperiod(self):
        current = Payperiod.objects.all().order_by('-due')[0]
        Payperiod.objects.all().order_by('-due')[0].delete()
        return current

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