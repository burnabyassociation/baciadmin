from django import forms 
from django.db import models

from mileage.models import Trip

class TripForm(forms.Form):
    class Meta:
        model = Trip

    trip_begin = forms.CharField(label="Odometer Start")
    trip_end = forms.CharField(label="Odometer End")
    description = forms.CharField(label="Trip Purpose")