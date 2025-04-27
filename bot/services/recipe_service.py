from asgiref.sync import sync_to_async
from random import choice
from decimal import Decimal
from recipes.models import RecipeStep, RecipeIngredient, Recipe
from bot.adapters.recipe_repository import DjangoRecipeRepository
from bot.adapters.feedback_repository import DjangoFeedbackRepository
from bot.adapters.user_repository import DjangoUserPreferencesRepository
from bot.logic.exceptions import RecipeNotFound, BotLogicError
import logging

logger = logging.getLogger(__name__)

class RecipeService:
    def __init__(self, recipe_repo, feedback_repo, prefs_repo):
        self._recipes = recipe_repo
        self._fb = feedback_repo
        self._prefs = prefs_repo

    async def fetch_random(self, telegram_id: int):
        prefs = await self._prefs.get(telegram_id)
        all_recipes = [
            r for r in await self._recipes.list_active()
            if (not prefs.vegan or r.is_vegan)
               and (not prefs.gluten_free or r.is_gluten_free)
               and (prefs.budget is None or r.estimated_cost <= prefs.budget)
        ]
        disliked = set(await self._fb.list_disliked(telegram_id))
        candidates = [r for r in all_recipes if r.id not in disliked]

        if not candidates:
            raise RecipeNotFound("Нет рецептов по вашим фильтрам.")
        return choice(candidates)

    @sync_to_async
    def save_feedback(self, telegram_id: int, recipe_id: int, kind: str):
        if kind not in ("like", "dislike"):
            raise BotLogicError("Feedback kind must be 'like' or 'dislike'")
        self._fb.save_feedback(telegram_id, recipe_id, kind)

    async def get_steps(self, recipe_id: int):
        steps_qs = await sync_to_async(RecipeStep.objects.filter)(recipe_id=recipe_id)
        steps = await sync_to_async(list)(steps_qs)
        steps.sort(key=lambda step: step.order)
        if not steps:
            raise RecipeNotFound("Шаги для рецепта не найдены.")
        return steps

    async def save_dislike(self, telegram_id: int, recipe_id: int):
        profile = await self._prefs.get(telegram_id)
        recipe = await self._recipes.get(recipe_id)
        await sync_to_async(profile.disliked.add)(recipe)
        await sync_to_async(profile.save)()

    @sync_to_async
    def get_ingredients(self, recipe_id: int):
        logger.info("Запрос ингредиентов для рецепта с ID %d", recipe_id)

        steps_qs = RecipeStep.objects.filter(recipe_id=recipe_id)
        steps = list(steps_qs)

        if not steps:
            raise RecipeNotFound("Шаги для рецепта не найдены.")

        ingredients = []

        for step in steps:
            logger.info("Обрабатываем шаг %d", step.id)

            recipe_ingredients_qs = RecipeIngredient.objects.filter(recipe=step.recipe).select_related('ingredient')
            recipe_ingredients = list(recipe_ingredients_qs)

            for ri in recipe_ingredients:
                ingredients.append(ri)  

        if not ingredients:
            raise RecipeNotFound("Ингредиенты для рецепта не найдены.")

        logger.info("Найдено ингредиентов: %d", len(ingredients))
        return ingredients


recipe_service = RecipeService(
    recipe_repo=DjangoRecipeRepository(),
    feedback_repo=DjangoFeedbackRepository(),
    prefs_repo=DjangoUserPreferencesRepository()
)

async def fetch_ingredients_for_recipe(recipe_id: int):
    try:
        ingredients = await recipe_service.get_ingredients(recipe_id)
        for ingredient in ingredients:
            print(f"{ingredient['name']} - {ingredient['amount']} {ingredient['unit']}")
    except RecipeNotFound as e:
        print(f"Ошибка: {e}")
