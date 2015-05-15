# mileage/views.py
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from mileage.models import Trip
#from mileage.models import User


class TripList(ListView):
    model = Trip

class TripCreate(CreateView):
	model = Trip
	fields = ['trip_begin','trip_end','description','paid']

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(TripCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse('mileage:list')