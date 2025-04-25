from bot.logic.interfaces import ISubscriptionRepository
from bot.logic.exceptions import SubscriptionError

class SubscriptionService:
    def __init__(self, sub_repo: ISubscriptionRepository):
        self._subs = sub_repo

    def check_active(self, telegram_id: int) -> bool:
        """Проверяет, есть ли у пользователя активная подписка."""
        try:
            return self._subs.is_active(telegram_id)
        except Exception as e:
            raise SubscriptionError(f"Ошибка при проверке подписки: {e}")

    def extend(self, telegram_id: int, days: int) -> None:
        """Продлевает подписку на days дней."""
        if days <= 0:
            raise SubscriptionError("Срок продления должен быть > 0")
        try:
            self._subs.extend(telegram_id, days)
        except Exception as e:
            raise SubscriptionError(f"Не удалось продлить подписку: {e}")
