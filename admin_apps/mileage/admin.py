from django.contrib import admin
from mileage.models import Trip, PayPeriod

def mark_as_paid(modeladmin, request, queryset):
    queryset.update(paid=True)
    

def mark_as_unpaid(modeladmin, request, queryset):
    queryset.update(paid=False)

class TripAdmin(admin.ModelAdmin):
    list_display= ('user','paid','approved','description')
    list_editable = ('paid','approved')
    actions = [mark_as_paid, mark_as_unpaid]

"""class PayPeriodInline(admin.StackedInline):
    model = PayPeriod
    extra = 3"""

class PayPeriodAdmin(admin.ModelAdmin):
	Model = PayPeriod
	extra = 3
    #inlines = [PayPeriodInline,]


admin.site.register(Trip, TripAdmin)
admin.site.register(PayPeriod, PayPeriodAdmin)