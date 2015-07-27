# mileage/views.py
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.template import RequestContext
from django.views import generic
from django.views.generic import detail
from django.db.models import Sum, Count, Max, Min
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView


from braces import views
from extra_views import ModelFormSetView, InlineFormSetView
from formtools.wizard.views import SessionWizardView

from mileage.models import Trip, Reimbursement
from mileage.forms import TripForm, ReimbursementForm
from adapters import FormsetMixin, RequiredInlineFormSet, get_total_amount_owed

class ReimbursementDetailView(DetailView):
    model = Reimbursement

    def get_context_data(self, **kwargs):
        context = super(ReimbursementDetailView, self).get_context_data(**kwargs)
        trips = Trip.objects.filter(reimbursement = self.object)
        #Other Context stuff
        context['trips'] = trips
        context['form'] = TripForm
        return context

#Creation View for Staff
class TripAddView(
    views.FormValidMessageMixin,
    generic.CreateView):
    """
    Handles post() in for the TripList View. Allows addition of trips.
    """
    form_valid_message = "Trip successfully added."
    template_name = 'mileage/reimbursement_detail.html'
    model = Trip
    fields = ('trip_begin', 'trip_end', 'description')
    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:detail_reimbursement', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        reimbursement = Reimbursement.objects.get(pk=self.kwargs['pk'])
        self.object.reimbursement = reimbursement
        self.object.save()
        return super(TripAddView, self).form_valid(form)

class TripListView(
    views.LoginRequiredMixin,
    generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    def get(self, request, *args, **kwargs):
        view = ReimbursementDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TripAddView.as_view()
        return view(request, *args, **kwargs)

class ReimbursementListView(ListView):

    model = Reimbursement
    def get_queryset(self):
        queryset = super(ReimbursementListView, self).get_queryset()
        queryset = queryset.filter(staff = self.request.user)
        return queryset

class ReimbursementCreateView(CreateView):
    model = Reimbursement
    success_url = reverse_lazy('mileage:home')
    fields = ['payperiod', 'department']


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.staff = self.request.user
        self.object.save()
        return super(ReimbursementCreateView, self).form_valid(form)
