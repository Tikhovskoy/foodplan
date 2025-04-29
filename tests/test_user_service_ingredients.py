import pytest
from datetime import timedelta
from django.utils import timezone

from users.models import TelegramUser, Profile
from bot.logic.user_service import UserService
from bot.adapters.user_repository import DjangoUserPreferencesRepository

pytestmark = pytest.mark.django_db


def test_user_with_subscription_can_view_ingredients():
    user = User.objects.create(username="subscriber", telegram_id=2001)
    profile = Profile.objects.create(user=user)
    profile.paid_until = timezone.now().date() + timedelta(days=1)
    profile.save()

    service = UserService(DjangoUserPreferencesRepository())
    assert service.can_view_ingredients(user.telegram_id) is True


def test_user_without_subscription_cannot_view_ingredients():
    user = User.objects.create(username="free_user", telegram_id=2002)
    Profile.objects.create(user=user)

    service = UserService(DjangoUserPreferencesRepository())
    assert service.can_view_ingredients(user.telegram_id) is False
