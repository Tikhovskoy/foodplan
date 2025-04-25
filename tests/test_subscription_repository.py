import pytest
from datetime import timedelta
from django.utils import timezone

from users.models import User, Profile
from bot.adapters.subscription_repository import DjangoSubscriptionRepository

@pytest.mark.django_db
def test_subscription_extend_and_check():
    user = User.objects.create(username="777")
    profile = Profile.objects.create(user=user)

    repo = DjangoSubscriptionRepository()

    assert not repo.is_active(telegram_id=777)

    repo.extend(telegram_id=777, days=3)
    profile.refresh_from_db()
    assert repo.is_active(telegram_id=777)
    assert profile.paid_until == timezone.now().date() + timedelta(days=3)
