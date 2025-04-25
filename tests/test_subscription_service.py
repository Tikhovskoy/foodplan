import unittest
from unittest.mock import MagicMock
from bot.logic.subscription_service import SubscriptionService
from bot.logic.exceptions import SubscriptionError

class TestSubscriptionService(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.service = SubscriptionService(sub_repo=self.repo)

    def test_check_active_success(self):
        self.repo.is_active.return_value = True
        result = self.service.check_active(telegram_id=123)
        self.assertTrue(result)
        self.repo.is_active.assert_called_once_with(123)

    def test_check_active_error(self):
        self.repo.is_active.side_effect = Exception("ошибка")
        with self.assertRaises(SubscriptionError):
            self.service.check_active(telegram_id=123)

    def test_extend_valid(self):
        self.service.extend(telegram_id=123, days=10)
        self.repo.extend.assert_called_once_with(123, 10)

    def test_extend_negative_days(self):
        with self.assertRaises(SubscriptionError):
            self.service.extend(telegram_id=123, days=-5)

    def test_extend_repo_failure(self):
        self.repo.extend.side_effect = Exception("база упала")
        with self.assertRaises(SubscriptionError):
            self.service.extend(telegram_id=123, days=30)


if __name__ == '__main__':
    unittest.main()
