# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from mileage.models import Trip
#from mileage.models import User

from braces import views

from mileage.forms import TripStartForm

class TripDisplay(
    generic.ListView):
    """
    Handles get() for the TripList View.
    """

    model = Trip
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TripDisplay, self).get_context_data(**kwargs)
        context['form'] = TripStartForm
        return context

class TripAdd(
    generic.CreateView):
    """
    Handles post() in for the TripList View. Allows addition of trips.
    """

    template_name = 'mileage/trip_list.html'
    model = Trip
    fields = ['trip_begin','description']

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
    Trip.objects.order_by('-create')
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
        

