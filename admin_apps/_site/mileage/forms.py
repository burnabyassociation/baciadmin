from django import forms 
from django.db import models

from mileage.models import Trip, PayPeriod

class TripStartForm(forms.Form):
    class Meta:
        model = Trip

    trip_begin = forms.CharField(label="Odometer Start")
    description = forms.CharField(label="Trip Purpose")

class PayPeriodAddForm(forms.Form):
    class Meta:
        model = PayPeriod

    date = forms.DateField(label="Date")