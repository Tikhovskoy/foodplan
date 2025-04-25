from datetime import timedelta
from django.utils import timezone

from bot.logic.interfaces import ISubscriptionRepository
from users.models import Profile


class DjangoSubscriptionRepository(ISubscriptionRepository):
    def is_active(self, telegram_id: int) -> bool:
        try:
            profile = Profile.objects.select_related("user").get(user__username=telegram_id)
            return profile.is_active_subscriber()
        except Profile.DoesNotExist:
            return False

    def extend(self, telegram_id: int, days: int) -> None:
        profile = Profile.objects.select_related("user").get(user__username=telegram_id)
        today = timezone.now().date()
        current = profile.paid_until or today
        new_date = max(today, current) + timedelta(days=days)
        profile.paid_until = new_date
        profile.save(update_fields=["paid_until"])
