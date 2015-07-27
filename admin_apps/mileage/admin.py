from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mileage.models import Trip, Reimbursement

class TripAdmin(admin.ModelAdmin):
	model = Trip
	search_fields = ['description','user__username']

class ReimbursementAdmin(admin.ModelAdmin):
    model = Reimbursement

admin.site.register(Trip, TripAdmin)
admin.site.register(Reimbursement, ReimbursementAdmin)