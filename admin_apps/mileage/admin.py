from django.contrib import admin
from mileage.models import Trip, PayPeriod

class TripAdmin(admin.ModelAdmin):

	def mark_as_paid(self, request, queryset):
	    rows_updated = queryset.update(paid=True)
	    if rows_updated == 1:
	        message_bit = "1 trip was"
	    else:
	        message_bit = "%s trips were" % rows_updated
	    self.message_user(request, "%s successfully marked as paid." % message_bit)

	def mark_as_unpaid(self, request, queryset):
	    queryset.update(paid=False)


	list_display= ('user','paid','approved','description')
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