# payments/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from .models import SubscriptionPlan, Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        # создаём тестовый тариф: 30 дней, цена 100 ₽
        self.plan = SubscriptionPlan.objects.create(
            name="Тестовый тариф",
            price=100.00,
            duration=30,
        )
        self.user = User.objects.create_user(username="tester", password="pass")

    def test_auto_dates_and_amount(self):
        """
        При создании Subscription(user, plan) метод save()
        должен установить start_date = сегодня,
        end_date = сегодня + plan.duration,
        amount = plan.price.
        """
        sub = Subscription.objects.create(user=self.user, plan=self.plan)
        today = date.today()
        sub.refresh_from_db()

        self.assertEqual(sub.start_date, today)
        self.assertEqual(sub.end_date, today + timedelta(days=self.plan.duration))
        self.assertEqual(float(sub.amount), float(self.plan.price))
