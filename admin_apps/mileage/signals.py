from django.db.models.signals import post_save
from mileage.models import Staff

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)