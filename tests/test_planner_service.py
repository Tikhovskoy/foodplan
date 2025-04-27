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
        self.service = PlannerService(engine=self.engine, prefs_repo=self.prefs_repo)

    def test_plan_week_success(self):
        prefs = UserPreferences(
            categories=[],
            vegan=False,
            gluten_free=False,
            budget=None,
            liked_recipes=[],
            disliked_recipes=[]
        )
        self.prefs_repo.get.return_value = prefs

        planned_meal = PlannedMeal()
        self.engine.plan_menu.return_value = [planned_meal]

        result = self.service.plan_week(telegram_id=123, start=date.today())
        self.assertEqual(result, [planned_meal])

        self.engine.plan_menu.assert_called_once_with(
            telegram_id=123,
            start=date.today(),
            days=7,
            prefs=prefs
        )

    def test_plan_week_failure(self):
        prefs = UserPreferences(
            categories=[],
            vegan=False,
            gluten_free=False,
            budget=None,
            liked_recipes=[],
            disliked_recipes=[]
        )
        self.prefs_repo.get.return_value = prefs

        self.engine.plan_menu.side_effect = Exception("Test error")

        with self.assertRaises(PlannerError):
            self.service.plan_week(telegram_id=123, start=date.today())

if __name__ == '__main__':
    unittest.main()
