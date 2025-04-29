from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"✅ Profile automatically created for user {instance.username} (tg id={instance.telegram_id})")
