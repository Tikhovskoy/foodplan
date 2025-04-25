import unittest
from unittest.mock import MagicMock
from datetime import date
from bot.logic.shopping_service import ShoppingService
from bot.logic.interfaces import UserPreferences, Recipe, Ingredient, PlannedMeal
from bot.logic.exceptions import ShoppingError

class TestShoppingService(unittest.TestCase):

    def setUp(self):
        self.planner_engine = MagicMock()
        self.prefs_repo = MagicMock()
        self.service = ShoppingService(
            planner_engine=self.planner_engine,
            prefs_repo=self.prefs_repo
        )

        self.prefs = UserPreferences()
        self.prefs.vegan = False
        self.prefs.gluten_free = False
        self.prefs.budget = None
        self.prefs_repo.get.return_value = self.prefs

    def _make_meal(self, name, amount, unit):
        ing = Ingredient()
        ing.name = name
        ing.amount = amount
        ing.unit = unit

        recipe = Recipe()
        recipe.id = 1
        recipe.title = "Test"
        recipe.description = "Test"
        recipe.ingredients = [ing]
        recipe.is_vegan = False
        recipe.is_gluten_free = False
        recipe.estimated_cost = 100

        meal = PlannedMeal()
        meal.recipe = recipe
        meal.date = date.today()

        return meal

    def test_build_list_returns_aggregated_items(self):
        meal1 = self._make_meal("картофель", 1.5, "кг")
        meal2 = self._make_meal("картофель", 2.0, "кг")
        meal3 = self._make_meal("морковь", 1.0, "шт")

        self.planner_engine.plan_menu.return_value = [meal1, meal2, meal3]

        result = self.service.build_list(telegram_id=123, start=date.today(), days=3)

        assert "3.50 кг картофель" in result
        assert "1.00 шт морковь" in result
        assert len(result) == 2

    def test_build_list_raises_on_planner_failure(self):
        self.planner_engine.plan_menu.side_effect = Exception("ошибка")

        with self.assertRaises(ShoppingError):
            self.service.build_list(telegram_id=123, start=date.today(), days=7)


if __name__ == '__main__':
    unittest.main()
