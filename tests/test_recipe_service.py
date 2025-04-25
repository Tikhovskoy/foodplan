import unittest
from unittest.mock import MagicMock
from bot.logic.recipe_service import RecipeService
from bot.logic.exceptions import RecipeNotFound, BotLogicError
from bot.logic.interfaces import Recipe, UserPreferences

class TestRecipeService(unittest.TestCase):

    def setUp(self):
        # Заглушки-репозитории
        self.recipe_repo = MagicMock()
        self.feedback_repo = MagicMock()
        self.prefs_repo = MagicMock()

        self.service = RecipeService(
            recipe_repo=self.recipe_repo,
            feedback_repo=self.feedback_repo,
            prefs_repo=self.prefs_repo
        )

        # Заглушка рецепта
        self.recipe = Recipe()
        self.recipe.id = 1
        self.recipe.title = "Тестовый рецепт"
        self.recipe.description = "Описание"
        self.recipe.is_vegan = True
        self.recipe.is_gluten_free = True
        self.recipe.estimated_cost = 200.0
        self.recipe.ingredients = []

    def test_fetch_random_returns_recipe(self):
        # Настройки пользователя
        prefs = UserPreferences()
        prefs.vegan = True
        prefs.gluten_free = True
        prefs.budget = 300.0

        self.prefs_repo.get.return_value = prefs
        self.recipe_repo.list_active.return_value = [self.recipe]
        self.feedback_repo.list_disliked.return_value = []

        result = self.service.fetch_random(telegram_id=123)
        self.assertEqual(result.id, self.recipe.id)

    def test_fetch_random_raises_if_no_recipe(self):
        prefs = UserPreferences()
        prefs.vegan = True
        prefs.gluten_free = True
        prefs.budget = 100.0  # меньше, чем стоимость рецепта

        self.prefs_repo.get.return_value = prefs
        self.recipe_repo.list_active.return_value = [self.recipe]
        self.feedback_repo.list_disliked.return_value = []

        with self.assertRaises(RecipeNotFound):
            self.service.fetch_random(telegram_id=123)

    def test_fetch_random_excludes_disliked(self):
        prefs = UserPreferences()
        prefs.vegan = True
        prefs.gluten_free = True
        prefs.budget = 500.0

        self.prefs_repo.get.return_value = prefs
        self.recipe_repo.list_active.return_value = [self.recipe]
        self.feedback_repo.list_disliked.return_value = [1]

        with self.assertRaises(RecipeNotFound):
            self.service.fetch_random(telegram_id=123)

    def test_save_feedback_valid(self):
        self.service.save_feedback(telegram_id=123, recipe_id=1, kind="like")
        self.feedback_repo.save_feedback.assert_called_once_with(123, 1, "like")

    def test_save_feedback_invalid_kind(self):
        with self.assertRaises(BotLogicError):
            self.service.save_feedback(telegram_id=123, recipe_id=1, kind="badvalue")


if __name__ == '__main__':
    unittest.main()
