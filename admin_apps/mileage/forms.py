from django import forms 
from django.db import models
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Field, Fieldset, Submit, Layout, ButtonHolder
from crispy_forms.bootstrap import StrictButton

from mileage.models import Trip, Payperiod, Staff

class StaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Staff
        exclude = ('user','slug')

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ('approved_by',)

class TripFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TripFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Fieldset('Reimbursements from this payperiod',
                Field('created'),
                Field('description'),
                Field('amount_owed'),
                Field('distance'),
                Field('paid'),
                Field('approved'),
                )
        )
        self.render_required_fields = True,

TripFormSet = inlineformset_factory(Staff, Trip, extra=0, fields='__all__')

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

class StaffTripFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(StaffTripFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Fieldset(
                'Edit the form',
                Field('trip_begin'),
                Field('trip_end'),
                Field('description'),
                Field('approved'),
                Field('paid')),
            ButtonHolder (
                Submit('add', 'Add', css_class='btn-primary')
                )
        )
        self.render_required_fields = True,