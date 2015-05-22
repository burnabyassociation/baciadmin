from django import forms 
from django.db import models

from mileage.models import Trip, Payperiod

class TripStartForm(forms.Form):
    class Meta:
        model = Trip

    trip_begin = forms.CharField(label="Odometer Start")
    description = forms.CharField(label="Trip Purpose")

class PayperiodAddForm(forms.Form):
    class Meta:
        model = Payperiod

    date = forms.DateField(label="Date")