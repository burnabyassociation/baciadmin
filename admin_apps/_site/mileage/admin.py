from django.contrib import admin
from mileage.models import Trip

class TripAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trip, TripAdmin)