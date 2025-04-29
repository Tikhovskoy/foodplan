from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Subscription
from users.models import TelegramUser

@receiver(post_save, sender=Subscription)
def update_user_paid_until(sender, instance, created, **kwargs):
    """
    При создании/обновлении подписки — копируем end_date → paid_until
    в вашей модели TelegramUser.
    """
    user, _ = TelegramUser.objects.get_or_create(
        telegram_id=instance.user.telegram_id,
        defaults={
            "username": instance.user.username or "",
            "first_name": instance.user.first_name or "",
            "last_name": instance.user.last_name or "",
        }
    )
    user.paid_until = instance.end_date
    user.save(update_fields=["paid_until"])
