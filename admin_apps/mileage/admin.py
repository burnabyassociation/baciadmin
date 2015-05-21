from django.contrib import admin
from mileage.models import Trip, PayPeriod

class TripAdmin(admin.ModelAdmin):
    list_display= ('user','paid','approved','description')
    search_fields = ['description']

"""class PayPeriodInline(admin.StackedInline):
    model = PayPeriod
    extra = 3"""

class PayPeriodAdmin(admin.ModelAdmin):
	Model = PayPeriod
	extra = 3
    #inlines = [PayPeriodInline,]


admin.site.register(Trip, TripAdmin)
admin.site.register(PayPeriod, PayPeriodAdmin)