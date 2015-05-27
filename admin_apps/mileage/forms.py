from django import forms 
from django.db import models
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder
from crispy_forms.bootstrap import StrictButton

from mileage.models import Trip, Payperiod

class TripStartForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripStartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'trip_begin',
            'description',
            ButtonHolder (
                Submit('next', 'Next', css_class='btn-primary')
                )
            )

    def clean(self):
        super(TripStartForm, self).clean()
        cleaned_data = self.cleaned_data
        trip_data = cleaned_data.get('trip_begin')
        if trip_data < 0:
            raise ValidationError("Beginning Mileage cannot be negative.")
        return cleaned_data

    class Meta:
        model = Trip
        fields = ['trip_begin', 'description']

class TripEndForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TripEndForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'trip_end',
            ButtonHolder (
                Submit('add', 'Add', css_class='btn-primary')
                )
            )
    def clean(self):
        super(TripEndForm, self).clean()
        cleaned_data = self.cleaned_data
        trip_data = cleaned_data.get('trip_end')
        if trip_data < Trip.trip_begin:
            raise ValidationError("Ending Mileage cannot be negative.")
        return cleaned_data

    class Meta:
        model = Trip
        fields = ['trip_end']

class ApproveForm(forms.Form):
    	approved = forms.BooleanField(label="Approved?")