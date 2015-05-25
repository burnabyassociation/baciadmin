# adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import Http404

class BACISocialAccountAdapter(DefaultSocialAccountAdapter):
	def populate_user(self, request, sociallogin, data):
		google_email = data.get('email')
		google_domain = google_email.split('@')[1]
		if not google_domain == "gobaci.com":
			raise Http404("Not a BACI Staff")
			
		user = super(BACISocialAccountAdapter, self).populate_user(request, sociallogin, data)
		return user