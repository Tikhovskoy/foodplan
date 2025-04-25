from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from users.models import UserPreferences
from bot.exceptions import BotError

User = get_user_model()

@sync_to_async
def ensure_user_exists(telegram_id: int):
    user, _ = User.objects.get_or_create(telegram_id=telegram_id)
    UserPreferences.objects.get_or_create(user=user)
    return user

@sync_to_async
def get_preferences(telegram_id: int):
    user = User.objects.get(telegram_id=telegram_id)
    prefs, _ = UserPreferences.objects.get_or_create(user=user)
    return prefs

@sync_to_async
def toggle_preference(telegram_id: int, field: str):
    user = User.objects.get(telegram_id=telegram_id)
    prefs, _ = UserPreferences.objects.get_or_create(user=user)
    if not hasattr(prefs, field):
        raise BotError("Неверная настройка")
    setattr(prefs, field, not getattr(prefs, field))
    prefs.save()
    return prefs
