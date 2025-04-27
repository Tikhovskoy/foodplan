class BotError(Exception):
    """Базовый класс ошибок бота."""
    pass

class RecipeNotFound(BotError):
    """Нет подходящих рецептов."""
    pass

class SubscriptionExpired(BotError):
    """Подписка истекла."""
    pass

class PreferenceError(Exception):
    """ Исключение для ошибок при работе с предпочтениями пользователя """
    pass

class BotLogicError(Exception):
    """ Исключение для ошибок логики бота """
    pass