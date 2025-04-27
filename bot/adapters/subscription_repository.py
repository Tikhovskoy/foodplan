# bot/adapters/subscription_repository.py

from asgiref.sync import sync_to_async
from datetime import timedelta, timezone
import random
import string
from django.db.models import Q
from users.models import Profile, User
from bot.logic.interfaces import ISubscriptionRepository  

class DjangoSubscriptionRepository(ISubscriptionRepository):

    @sync_to_async
    def _get_profile(self, telegram_id: int) -> Profile:
        """
        Возвращает профиль пользователя, пытаясь сначала по telegram_id, затем по username.
        """
        return Profile.objects.select_related("user").get(
            Q(user__telegram_id=telegram_id) | Q(user__username=str(telegram_id))
        )

    @sync_to_async
    def is_active(self, telegram_id: int) -> bool:
        """
        Проверяет, есть ли у пользователя активная подписка.
        """
        try:
            profile = self._get_profile(telegram_id)
            return profile.is_active_subscriber()
        except Profile.DoesNotExist:
            return False

    async def extend(self, telegram_id: int, days: int) -> None:
        """
        Продлевает подписку пользователя на указанное число дней.
        Автоматически создаёт профиль, если он не существует.
        """
        try:
            profile = await self._get_profile(telegram_id)  
        except Profile.DoesNotExist:
            await self.create_profile(telegram_id)
            profile = await self._get_profile(telegram_id)

        today = timezone.now().date()
        current = profile.paid_until or today
        new_date = max(today, current) + timedelta(days=days)
        profile.paid_until = new_date
        profile.save()

    async def create_profile(self, telegram_id: int):
        """
        Создаёт нового пользователя и профиль в базе данных.
        Гарантирует уникальный username.
        """
        base_username = f"user_{telegram_id}"
        username = base_username

        while User.objects.filter(username=username).exists():
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{base_username}_{suffix}"

        user = User.objects.create(username=username, telegram_id=telegram_id)
        Profile.objects.create(user=user)
