from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import Profile
from payments.models import Subscription, SubscriptionPlan


class SubscriptionModelTest(TestCase):
    def test_profile_paid_until_sync(self):
        """
        paid_until в профиле синхронизируется с end_date подписки,
        при этом все даты и сумма рассчитываются в save().
        """
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="pass")

        profile = Profile.objects.get(user=user)

        plan = SubscriptionPlan.objects.create(
            name="Тестовый тариф",
            price=100,
            duration=30,  
        )

        subscription = Subscription.objects.create(user=user, plan=plan)

        expected_end = date.today() + timedelta(days=plan.duration)

        self.assertEqual(subscription.end_date, expected_end)
        self.assertEqual(float(subscription.amount), float(plan.price))

        profile.refresh_from_db()
        self.assertEqual(
            profile.paid_until,
            expected_end,
            "paid_until в профиле должен совпадать с end_date подписки"
        )
