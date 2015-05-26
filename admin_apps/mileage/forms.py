from django import forms 
from django.db import models

from mileage.models import Trip, Payperiod

class TripStartForm(forms.Form):
    	trip_begin = forms.CharField(label="Odometer Start")
    	description = forms.CharField(label="Trip Purpose")

class TripEndForm(forms.Form):
    	trip_end = forms.CharField(label="Odometer End")

"""class PayperiodAddForm(forms.Form):
    class Meta:
        model = Payperiod

    due = forms.DateField(label="Due")
"""