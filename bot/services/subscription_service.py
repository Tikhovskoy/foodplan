from payments.models import Subscription, SubscriptionPlan
from users.models import TelegramUser
from django.utils import timezone
from datetime import timedelta

class SubscriptionService:
    async def get_active_subscription(self, user: TelegramUser):
        """Получить активную подписку пользователя."""
        now = timezone.now()
        return await Subscription.objects.filter(user=user, end_date__gte=now).afirst()

    async def is_subscription_active(self, user: TelegramUser) -> bool:
        """Проверить активность подписки."""
        subscription = await self.get_active_subscription(user)
        return subscription is not None

    async def create_subscription(self, user: TelegramUser, plan: SubscriptionPlan):
        """Создать новую подписку для пользователя."""
        end_date = timezone.now() + timedelta(days=30)
        return await Subscription.objects.acreate(user=user, plan=plan, end_date=end_date)

subscription_service = SubscriptionService()
