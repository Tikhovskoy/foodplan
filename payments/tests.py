from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile
from payments.models import Subscription, SubscriptionPlan


class SubscriptionModelTest(TestCase):
    def test_profile_paid_until_sync(self):
        """
        paid_until в профиле синхронизируется с end_date подписки
        """
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="12345")
        profile = Profile.objects.get(user=user)

        plan = SubscriptionPlan.objects.create(
            name="Тестовый",
            price=199,
            duration=30,  # в днях
        )

        today = date.today()
        expected_end_date = today + timedelta(days=plan.duration)

        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=today,
            end_date=expected_end_date,
            amount=plan.price
        )

        profile.refresh_from_db()
        self.assertEqual(
            profile.paid_until,
            expected_end_date,
            "paid_until в профиле не совпадает с end_date подписки"
        )
