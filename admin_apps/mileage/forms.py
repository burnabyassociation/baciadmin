from django import forms 
from django.db import models

from mileage.models import Trip

class TripStartForm(forms.Form):
    class Meta:
        model = Trip

    trip_begin = forms.CharField(label="Odometer Start")
    description = forms.CharField(label="Trip Purpose")