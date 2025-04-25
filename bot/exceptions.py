class BotError(Exception):
    """Базовый класс ошибок бота."""
    pass

class RecipeNotFound(BotError):
    """Нет подходящих рецептов."""
    pass

class SubscriptionExpired(BotError):
    """Подписка истекла."""
    pass
