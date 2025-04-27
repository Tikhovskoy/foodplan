from datetime import date, timedelta
from typing import List

from bot.logic.interfaces import (
    IPlannerEngine,
    IRecipeRepository,
    IFeedbackRepository,
    IUserPreferencesRepository,
    PlannedMeal,
)
from bot.logic.exceptions import PlannerError

class SimplePlannerEngine(IPlannerEngine):
    """
    Простой движок: на каждый день собирает одну порцию (случайный рецепт)
    с учётом настроек пользователя.
    """

    def __init__(
        self,
        recipe_repo: IRecipeRepository,
        feedback_repo: IFeedbackRepository,
        prefs_repo: IUserPreferencesRepository,
    ):
        self._recipes = recipe_repo
        self._feedback = feedback_repo
        self._prefs = prefs_repo

    def plan_menu(
        self,
        telegram_id: int,
        start: date,
        days: int,
        prefs,  
    ) -> List[PlannedMeal]:
        meals: List[PlannedMeal] = []
        try:
            for offset in range(days):
                run_date = start + timedelta(days=offset)

                from bot.logic.recipe_service import RecipeService
                recipe_service = RecipeService(
                    recipe_repo=self._recipes,
                    feedback_repo=self._feedback,
                    prefs_repo=self._prefs
                )
                recipe = recipe_service.fetch_random(telegram_id=telegram_id)

                pm = PlannedMeal()
                pm.recipe = recipe
                pm.date = run_date
                meals.append(pm)
            return meals

        except Exception as e:
            raise PlannerError(f"Ошибка в движке планирования: {e}")
