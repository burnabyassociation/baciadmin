# adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import Http404
from django.contrib.auth.models import User
from mileage.models import Trip, Payperiod
from django.db.models import Sum
from django.utils import timezone


class BACISocialAccountAdapter(DefaultSocialAccountAdapter):
	def populate_user(self, request, sociallogin, data):
		google_email = data.get('email')
		google_domain = google_email.split('@')[1]
		if not google_domain == "gobaci.com":
			raise Http404("Not a BACI Staff")
			
		user = super(BACISocialAccountAdapter, self).populate_user(request, sociallogin, data)
		return user

def get_total_amount_owed(User):
		total = Trip.objects.filter(user=User).aggregate(total=Sum('amount_owed'))
   		return total

def get_current_payperiod():
        periods = Payperiod.objects.all().order_by('due')
        if periods.exists():
	        for period in periods:
	            if period.due < timezone.now().date():
	                period.delete()
	        return periods[0]
