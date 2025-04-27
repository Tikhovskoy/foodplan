from random import choice
from typing import List
from bot.logic.interfaces import (
    IRecipeRepository,
    IFeedbackRepository,
    IUserPreferencesRepository,
    Recipe
)
from bot.logic.exceptions import RecipeNotFound, BotLogicError

class RecipeService:
    def __init__(
        self,
        recipe_repo: IRecipeRepository,
        feedback_repo: IFeedbackRepository,
        prefs_repo: IUserPreferencesRepository
    ):
        self._recipes = recipe_repo
        self._fb = feedback_repo
        self._prefs = prefs_repo

    def fetch_random(self, telegram_id: int) -> Recipe:
        """
        Возвращает случайный рецепт по prefs, без ранее дизлайкнутых.
        Бросает RecipeNotFound.
        """
        prefs = self._prefs.get(telegram_id)
        all_recipes = [
            r for r in self._recipes.list_active()
            if (not prefs.vegan or r.is_vegan)
               and (not prefs.gluten_free or r.is_gluten_free)
               and (prefs.budget is None or r.estimated_cost <= prefs.budget)
        ]
        disliked = set(self._fb.list_disliked(telegram_id))
        candidates = [r for r in all_recipes if r.id not in disliked]

        if not candidates:
            raise RecipeNotFound("Нет рецептов по вашим фильтрам.")
        return choice(candidates)

    def save_feedback(self, telegram_id: int, recipe_id: int, kind: str) -> None:
        """
        Сохраняет лайк/дизлайк.
        kind — 'like' или 'dislike'
        """
        if kind not in ("like", "dislike"):
            raise BotLogicError("Feedback kind must be 'like' or 'dislike'")
        self._fb.save_feedback(telegram_id, recipe_id, kind)

    def get_recipe(self, recipe_id: int) -> Recipe:
        """
        Возвращает рецепт по ID.
        Бросает RecipeNotFound, если рецепт не найден.
        """
        recipe = self._recipes.get(recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Рецепт с ID {recipe_id} не найден.")
        return recipe