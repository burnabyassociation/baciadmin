# adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import Http404
from django.contrib.auth.models import User
from mileage.models import Trip, Payperiod
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import redirect
from django.forms.models import BaseInlineFormSet


class BACISocialAccountAdapter(DefaultSocialAccountAdapter):
	def populate_user(self, request, sociallogin, data):
		google_email = data.get('email')
		google_domain = google_email.split('@')[1]
		if not google_domain == "gobaci.com":
			raise Http404("Not a BACI Staff")
			
		user = super(BACISocialAccountAdapter, self).populate_user(request, sociallogin, data)
		return user

class RequiredInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
            
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        if hasattr(self, 'get_success_message'):
            self.get_success_message(form)
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

def get_total_amount_owed(User):
		total = Trip.objects.filter(user=User).aggregate(total=Sum('amount_owed'))
   		return total

def get_current_payperiod():
        periods = Payperiod.objects.all().order_by('due')
        if periods.exists():
	        for period in periods:
	            if period.due < timezone.now().date():
	                period.delete()
	        return periods[0]
