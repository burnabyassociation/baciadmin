from django import forms 
from django.db import models
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Field, Fieldset, Submit, Layout, ButtonHolder
from crispy_forms.bootstrap import StrictButton
from datetimewidget.widgets import DateTimeWidget

from mileage.models import Trip, Reimbursement

class ReimbursementForm(forms.ModelForm):
    class Meta:
        model = Reimbursement
        exclude = ('user','slug')

    def __init__(self, *args, **kwargs):
        super(ReimbursementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                Field('payperiod', css_class="col-lg-6 mileage-input"),
                Field('department', css_class="col-lg-6 mileage-input"),
            ButtonHolder (
                Submit('add', 'Add', css_class='btn-primary pull-right')
                )
            ) 
        )

class TripForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('trip_begin', type="number", placeholder="Record your starting mileage", css_class="col-md-6"),
            Field('trip_end', type="number", placeholder="Record your ending mileage", css_class="mileage-input"),
            Field('description', css_class="mileage-input"),
            HTML("<h4 style='padding-left:12px;'><small>*If using an odometer, record 0.</small></h4>"),
            ButtonHolder (
                Submit('next', 'Next', css_class='btn-primary pull-right')
                )
            )

    def clean(self):
        super(TripForm, self).clean()
        cleaned_data = self.cleaned_data
        trip_data = cleaned_data.get('trip_begin')
        if trip_data < 0:
            raise ValidationError("Beginning Mileage cannot be negative.")
        return cleaned_data

    class Meta:
        widgets = {
            #Use localization and bootstrap 3
            'trip_date': DateTimeWidget(attrs={'id':"date_time"}, usel10n = True, bootstrap_version=3)
        }
        model = Trip
        fields = ['trip_date', 'trip_begin', 'trip_end', 'description']
