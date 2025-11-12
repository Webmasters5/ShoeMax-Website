from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    # Automatically create a Customer when a User is created
    if created and not hasattr(instance, 'customer'):
        Customer.objects.create(user=instance)
