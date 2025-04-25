import unittest
from unittest.mock import MagicMock
from datetime import date
from bot.logic.planner_service import PlannerService
from bot.logic.interfaces import UserPreferences, PlannedMeal
from bot.logic.exceptions import PlannerError

class TestPlannerService(unittest.TestCase):

    def setUp(self):
        self.engine = MagicMock()
        self.prefs_repo = MagicMock()

        self.service = PlannerService(
            engine=self.engine,
            prefs_repo=self.prefs_repo
        )

        self.prefs = UserPreferences()
        self.prefs.vegan = False
        self.prefs.gluten_free = False
        self.prefs.budget = None

        self.prefs_repo.get.return_value = self.prefs

    def test_plan_week_success(self):
        planned = PlannedMeal()
        self.engine.plan_menu.return_value = [planned]

        result = self.service.plan_week(telegram_id=123, start=date.today())

        self.assertEqual(result, [planned])
        self.engine.plan_menu.assert_called_once_with(
            telegram_id=123,
            start=date.today(),
            days=7,
            prefs=self.prefs
        )

    def test_plan_week_raises_on_error(self):
        self.engine.plan_menu.side_effect = Exception("ошибка движка")

        with self.assertRaises(PlannerError):
            self.service.plan_week(telegram_id=123, start=date.today())


if __name__ == '__main__':
    unittest.main()
