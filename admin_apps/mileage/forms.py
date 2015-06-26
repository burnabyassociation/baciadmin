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
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('trip_begin', type="number", placeholder="Record your starting mileage", css_class="mileage-input"),
            Field('trip_end', type="hidden", placeholder="Record your ending mileage"),
            HTML("<h4 style='padding-left:12px;'><small>*If using an odometer, record 0.</small></h4>"),
            ButtonHolder (
                Submit('next', 'Next', css_class='btn-primary pull-right')
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
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                "<h4>Finish by filling in the ending mileage and the description of your trip.</h4>",
                Field('trip_begin', type="number", css_class="col-lg-6 mileage-input"),
                Field('trip_end', type="number", placeholder="Record your ending mileage", css_class="col-lg-6 mileage-input"),
                Field('description', placeholder="Write a description of your trip", css_class="mileage-input")),
            ButtonHolder (
                Submit('add', 'Add', css_class='btn-primary pull-right')
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
            raise ValidationError("Ending mileage cannot be less than beginning mileage.")
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