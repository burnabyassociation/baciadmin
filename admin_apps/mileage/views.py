# mileage/views.py

from django.views.generic import ListView
from mileage.models import Trip


class TripList(ListView):
    model = Trip