# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from mileage.models import Trip, Payperiod
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView

from braces import views
from extra_views import ModelFormSetView

from mileage.forms import TripStartForm, TripEndForm

#uses django-formtools to create a 2 step form using one model
#need to add logic to save form
class TripWizard(SessionWizardView):
    template_name = 'mileage/trip_wizardform.html'
    form_list = [TripStartForm, TripEndForm]

    def done(self, form_list, **kwargs):
        return reverse('mileage:list')

#uses django-extra-views to create a multiformset
#need to add logic to bulk save edits
class SupervisorFormView(
    ModelFormSetView):
    template_name = "mileage/trip_formset.html"
    model = Trip
    fields = ('user','trip_begin', 'trip_end','paid','approved')

    def get_queryset(self):
        try:
            group = self.request.user.groups.all()[0]
            user_list = User.objects.filter(groups__name=group)
        except:
            pass
        return super(SupervisorFormView, self).get_queryset().filter(paid=False)


class TripDisplayView(
    generic.ListView):
    """
    Handles get() for the TripList View.
    """
    model = Trip

    def get_current_payperiod(self):
        periods = Payperiod.objects.all().order_by('due')
        for period in periods:
            if period.due < timezone.now().date():
                period.delete()
        return periods[0]

    def get_context_data(self, **kwargs):
        context = super(TripDisplay, self).get_context_data(**kwargs)
        context['form'] = TripStartForm
        context['current'] = self.get_current_payperiod()
        return context

    def get_queryset(self):
        queryset = super(TripDisplay, self).get_queryset()
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
        return super(TripAdd, self).form_valid(form)

class TripListView(
    views.LoginRequiredMixin,
    generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    def get(self, request, *args, **kwargs):
        view = TripDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TripAdd.as_view()
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
        

