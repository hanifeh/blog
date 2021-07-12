from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from store.signals import order_placed


@receiver(order_placed)
def send_email_when_order_is_placed(sender, **kwargs):

    print('your order received .')


@receiver(post_save)
def create_profile_for_user(sender, **kwargs):
    if 'django.contrib.auth.models.User' in str(sender) and kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
