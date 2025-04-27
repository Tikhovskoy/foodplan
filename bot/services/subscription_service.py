from bot.logic.subscription_service import SubscriptionService
from bot.adapters.subscription_repository import DjangoSubscriptionRepository

class SubscriptionServiceWrapper:
    def __init__(self):
        repository = DjangoSubscriptionRepository()
        self._service = SubscriptionService(repository)

    async def check_active(self, telegram_id: int) -> bool:
        return self._service.is_active(telegram_id)

    async def extend_subscription(self, telegram_id: int, days: int) -> None:
        self._service.extend_subscription(telegram_id, days)

subscription_service = SubscriptionServiceWrapper()
