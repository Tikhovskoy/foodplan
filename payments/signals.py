from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Subscription
from users.models import Profile


@receiver(post_save, sender=Subscription)
def update_profile_paid_until(sender, instance, **kwargs):
    """
    При создании или обновлении подписки копируем end_date в user.profile.paid_until.
    """
    profile = instance.user.profile
    profile.paid_until = instance.end_date
    profile.save(update_fields=["paid_until"])
