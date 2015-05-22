# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from mileage.models import Trip, Payperiod
from django.utils import timezone
#from mileage.models import User

from braces import views

from mileage.forms import TripStartForm

class PayperiodList(generic.ListView):
    model = Payperiod

    def get_current(self):
        periods = Payperiod.objects.all().order_by('due')
        for period in periods:
            if period.due < timezone.now().date():
                period.delete()
        return periods[0]

    def get_context_data(self, **kwargs):
        context = super(PayperiodList, self).get_context_data(**kwargs)
        context['current'] = self.get_current()
        return context

    """
class PayperiodList(generic.View):
    Payperiod.objects.order_by('-due')
    def get(self, request, *args, **kwargs):
        view = PayperiodDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PayperiodAdd.as_view()
        return view(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mileage:payperiodlist')


class PayperiodDisplay(generic.ListView):
    model = Payperiod
    def get_context_data(self, **kwargs):
        context = super(PayperiodDisplay, self).get_context_data(**kwargs)
        context['payperiods']=Payperiod.objects.all()
        context['current']=Payperiod.get_current_pay_period()
        context['form']=PayperiodAdmin
        return context

    def get_queryset(self):
        queryset = super(PayperiodDisplay, self).get_queryset()
        queryset = queryset.order_by('-due')
        return queryset
"""

class PayperiodAdd(generic.CreateView):

    model = Payperiod
    fields = ('due')
    
    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:payperiod', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PayperiodAdd, self).form_valid(form)


#Trip Stuff
class TripDisplay(
    generic.ListView):
    """
    Handles get() for the TripList View.
    """
    model = Trip
    paginate_by = 10

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

class TripAdd(
    generic.CreateView):
    """
    Handles post() in for the TripList View. Allows addition of trips.
    """

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

class TripList(generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    def get(self, request, *args, **kwargs):
        view = TripDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TripAdd.as_view()
        return view(request, *args, **kwargs)


class TripEdit(generic.UpdateView):
    template_name = 'mileage/trip_edit.html'
    model = Trip
    fields = ['trip_end']
    def get_success_url(self):
        return reverse('mileage:list')
        

