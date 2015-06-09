from django import forms 
from django.db import models
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Submit, Layout, ButtonHolder
from crispy_forms.bootstrap import StrictButton

from mileage.models import Trip, Payperiod

class TripStartForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripStartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('Enter your starting mileage or 0 for an odometer.',
                Field('trip_begin', type="number")),

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
        fields = ['trip_begin']

class TripEndForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TripEndForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Finish the form by filling in the ending mileage and the description of your trip.',
                Field('trip_begin'),
                Field('trip_end'),
                Field('description')),
            ButtonHolder (
                Submit('add', 'Add', css_class='btn-primary')
                )
            )

    def clean(self):
        super(TripEndForm, self).clean()
        cleaned_data = self.cleaned_data
        trip_begin = cleaned_data.get('trip_begin')
        trip_end = cleaned_data.get('trip_end')
        if trip_end < 0:
            raise ValidationError("Ending Mileage cannot be negative.")
        if trip_end < trip_begin:
            raise ValidationError("Ending mileage cannot be less than beginning.")
        return cleaned_data

    class Meta:
        model = Trip
        fields = ['trip_begin','trip_end', 'description']

class ApproveForm(forms.Form):
    	approved = forms.BooleanField(label="Approved?")