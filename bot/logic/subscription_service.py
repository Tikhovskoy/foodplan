from bot.adapters.subscription_repository import DjangoSubscriptionRepository

class SubscriptionService:
    def __init__(self, repository: DjangoSubscriptionRepository):
        self._repository = repository

    def is_active(self, telegram_id: int) -> bool:
        """ Проверяет активность подписки. """
        return self._repository.is_active(telegram_id)

    def extend_subscription(self, telegram_id: int, days: int) -> None:
        """ Продлевает подписку на заданное количество дней. """
        self._repository.extend(telegram_id, days)
