# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.db.models import Sum, Count, Max, Min
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory


from braces import views
from extra_views import ModelFormSetView, InlineFormSetView
from formtools.wizard.views import SessionWizardView

from mileage.models import Trip, Payperiod, Staff
from mileage.forms import TripFormHelper, TripFormSet, TripForm, TripStartForm, TripEndForm, StaffTripFormSetHelper, StaffForm
from adapters import FormsetMixin, RequiredInlineFormSet, get_total_amount_owed, get_current_payperiod


#This is the user profile view that supervisors and admin access to approve/pay localhost/1/edit
class StaffView(FormsetMixin, UpdateView):
    template_name = 'mileage/staff.html'
    is_update_view = True
    model = Staff
    form_class = StaffForm
    formset_class = TripFormSet

    def get_formset_kwargs(self):
        kwargs = super(StaffView, self).get_formset_kwargs()
        if 'admins' in self.request.user.groups.values_list('name', flat=True):
            kwargs['queryset'] = Trip.objects.filter(staff=self.object, paid=False, approved=True)
        else:
            kwargs['queryset'] = Trip.objects.filter(staff=self.object, paid=False, approved=False)
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(StaffView, self).get_context_data(**kwargs)
        context['helper'] = TripFormHelper()
        context['approved_trips'] = Trip.objects.filter(staff=self.object, approved=True)
        context['current'] = get_current_payperiod()
        try:
            context['supervisor'] = Group.objects.get(name='Supervisors')
            context['admin'] = Group.objects.get(name='Admins')
        except:
            pass
        return context

#This is the staff's add trip view
class TripWizard(views.LoginRequiredMixin,
    SessionWizardView):
    template_name = 'mileage/trip_wizardform.html'
    form_list = [TripStartForm, TripEndForm]
    model = Trip
    
    def get_form_initial(self, step):
        if step == '1':
            data = self.get_cleaned_data_for_step('0') or {}
            return data
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        instance = Trip()
        instance.staff = self.request.user.staff
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                setattr(instance, field, value)
        instance.save()
        messages.success(self.request, 'Reimbursement %s added.' % instance)
        return redirect('mileage:wizard')

#this is the supervisor dashbaord view
class SupervisorDashboardView(
    generic.TemplateView):
    template_name = "mileage/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(SupervisorDashboardView, self).get_context_data(**kwargs)
        try:
            group = self.request.user.groups.all()[0]
            user_list = User.objects.filter(groups__name__in=[group]).filter(staff__trip__approved=False)
            user_list = user_list.annotate(reimbursement=Sum('staff__trip__amount_owed')) #total amount owed
            user_list = user_list.annotate(total_mileage=Sum('staff__trip__distance')) #total distance travelled
            user_list  = user_list.annotate(num_trips=Count('staff__trip')) #total amount of reimbursements
            user_list = user_list.annotate(oldest_trip=Min('staff__trip__created'))
            user_list = user_list.annotate(newest_trip=Max('staff__trip__created'))
        except:
            user_list = []
        context['user_list'] = user_list
        context['current'] = get_current_payperiod()
        return context

#This is the generic list view
class TripDisplayView(
    generic.ListView):
    """
    Handles get() for the TripList View.`
    """
    model = Trip


    def get_context_data(self, **kwargs):
        context = super(TripDisplayView, self).get_context_data(**kwargs)
        context['current'] = get_current_payperiod()
        return context

    def get_queryset(self):
        queryset = super(TripDisplayView, self).get_queryset()
        queryset = queryset.order_by('-created')
        return queryset

#Creation View for Staff
class TripAddView(
    views.FormValidMessageMixin,
    generic.CreateView):
    """
    Handles post() in for the TripList View. Allows addition of trips.
    """
    form_valid_message = "Trip Started. Please add an ending mileage."
    template_name = 'mileage/trip_list.html'
    model = Trip
    fields = ('trip_begin', 'description')
    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TripAddView, self).form_valid(form)

class TripListView(
    views.LoginRequiredMixin,
    generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    def get(self, request, *args, **kwargs):
        view = TripDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TripAddView.as_view()
        return view(request, *args, **kwargs)

