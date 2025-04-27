class BotLogicError(Exception):
    """Базовое исключение бизнес-логики."""

class RecipeNotFound(BotLogicError):
    """Нет подходящих рецептов."""

class PreferenceError(BotLogicError):
    """Ошибка при работе с настройками пользователя."""

class SubscriptionError(BotLogicError):
    """Ошибка при проверке/продлении подписки."""

class PlannerError(BotLogicError):
    """Ошибка при составлении плана питания."""

class ShoppingError(BotLogicError):
    """Ошибка при генерации списка покупок."""

class BotError(BotLogicError):
    """Общее исключение для адаптеров Telegram-бота."""

class RecipeAlreadyLiked(Exception):
    pass

class RecipeAlreadyDisliked(Exception):
    pass

class DailyLimitReached(Exception):
    pass
