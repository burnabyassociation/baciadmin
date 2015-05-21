from django.contrib import admin
from mileage.models import Trip, PayPeriod

class TripAdmin(admin.ModelAdmin):
    pass

#class PayPeriodInline(admin.StackedInline):
#    model = PayPeriod
#    extra = 3

class PayPeriodAdmin(admin.ModelAdmin):
	pass
    #fieldsets = [
    #    ('Due',               {'fields': ['due']}),
    #]
    #inlines = [PayPeriodInline]
    #pass

admin.site.register(Trip, TripAdmin)
admin.site.register(PayPeriod, PayPeriodAdmin)