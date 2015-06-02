# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from braces import views
from extra_views import ModelFormSetView, InlineFormSetView
from formtools.wizard.views import SessionWizardView

from mileage.models import Trip, Payperiod, StaffProfile
from mileage.forms import TripStartForm, TripEndForm, ApproveForm
from adapters import get_total_amount_owed, get_current_payperiod


#uses django-formtools to create a 2 step form using one model
#need to add logic to save form
class TripWizard(SessionWizardView):
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
        instance.user = self.request.user
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                setattr(instance, field, value)
        instance.save()
        return redirect('mileage:list')

class SupervisorDashboardView(
    generic.TemplateView):

    template_name = "mileage/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(SupervisorDashboardView, self).get_context_data(**kwargs)
        try:
            group = self.request.user.groups.all()[0]
            staff_list = User.objects.filter(groups__name__in=[group]).filter(trip__approved=False)
            staff_list = staff_list.annotate(reimbursement=Sum('trip__amount_owed')).annotate(total_mileage=Sum('trip__distance'))
        except:
            staff_list = []
        context['staff_list'] = staff_list
        context['current'] = get_current_payperiod()
        return context

class StaffDetailView(
    generic.DetailView):
    model = User

class StaffReimbursementView(
    InlineFormSetView):
    model = StaffProfile
    inline_model = Trip
    
    template_name = "mileage/user.html"

#uses django-extra-views to create a multiformset
#need to add logic to bulk save edits
class UserListView(generic.ListView):
    template_name = "mileage/user_list.html"
    model = Trip
    fields = ['user','created','trip_begin','trip_end','paid','approved']


class SupervisorFormView(
    ModelFormSetView):
    template_name = "mileage/trip_formset.html"
    model = Trip
    fields = ['user','created','trip_begin','trip_end','paid','approved']

#    def get_total_amount_owed(self):
 #       total = .aggregate(total=Sum('amount_owed'))
  #      return total

    def get_context_data(self, **kwargs):
        context = super(SupervisorFormView, self).get_context_data(**kwargs)

        group = self.request.user.groups.all()[0]
        users = User.objects.all().filter(groups__name__in=[group])
        total_reimbursements = []
        for user in users:
            total_reimbursements.append(get_total_amount_owed(user))

        context['form'] = ApproveForm
        context['user_list'] = users
        context['reimbursements'] = total_reimbursements
        context['current'] = get_current_payperiod()
        return context

    def get_queryset(self):
        try:
            group = self.request.user.groups.all()[0]
            return super(SupervisorFormView, self).get_queryset().filter(user__groups__name__in=[group]).filter(paid=False)
        except:
            pass
        return super(SupervisorFormView, self).get_queryset().filter(paid=False).order_by('user').distinct('user')

    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:supervisor', kwargs={'pk': self.object.pk})

class TripDisplayView(
    generic.ListView):
    """
    Handles get() for the TripList View.`
    """
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripDisplayView, self).get_context_data(**kwargs)
        context['form'] = ApproveForm
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
        return reverse('mileage:edit', kwargs={'pk': self.object.pk})

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


class TripEditView(
    views.FormValidMessageMixin,
    generic.UpdateView):

    form_valid_message = "Trip Reimbursement Added."
    template_name = 'mileage/trip_edit.html'
    model = Trip
    fields = ['trip_end']
    def get_success_url(self):
        return reverse('mileage:list')
        

