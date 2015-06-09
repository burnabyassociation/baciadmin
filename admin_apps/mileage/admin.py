from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mileage.models import Trip, Payperiod, Staff

class TripAdmin(admin.ModelAdmin):

	def mark_as_paid(self, request, queryset):
	    rows_updated = queryset.update(paid=True)
	    if rows_updated == 1:
	        message_bit = "1 trip was"
	    else:
	        message_bit = "%s trips were" % rows_updated
	    self.message_user(request, "%s successfully marked as paid." % message_bit)

	def mark_as_unpaid(self, request, queryset):
	    rows_updated = queryset.update(paid=False)
	    if rows_updated == 1:
	        message_bit = "1 trip was"
	    else:
	        message_bit = "%s trips were" % rows_updated
	    self.message_user(request, "%s successfully marked as unpaid." % message_bit)
	list_display= ('staff','paid','approved','description')
	list_filter=(
		('paid', admin.BooleanFieldListFilter),'approved'
    )
	actions = [mark_as_paid, mark_as_unpaid]
	search_fields = ['description','user__username']

class PayperiodAdmin(admin.ModelAdmin):
    model = Payperiod
    list_display= ('due','created')

class StaffInline(admin.StackedInline):
	model = Staff
	can_delete = False
	verbose_name_plural = "staff"

class Useradmin(UserAdmin):
	inlines = (StaffInline, )

admin.site.unregister(User)
admin.site.register(Trip, TripAdmin)
admin.site.register(Payperiod, PayperiodAdmin)
admin.site.register(User, Useradmin)