from random import choice
from asgiref.sync import sync_to_async
from recipes.models import Recipe, RecipeStep, Ingredient
from users.models import TelegramUser
from typing import Optional



class RecipeService:
    async def fetch_random_by_meal_and_category(self, meal_time_id: int, category_id: int) -> Optional[Recipe]:
        recipes = await sync_to_async(list)(
            Recipe.objects.filter(
                is_active=True,
                meal_times__id=meal_time_id,
                categories__id=category_id
            ).distinct()
        )
        return choice(recipes) if recipes else None

    async def fetch_all_by_meal_and_category(self, meal_time_id: int, category_id: int):
        return await sync_to_async(list)(
            Recipe.objects.filter(
                meal_times__id=meal_time_id,
                categories__id=category_id,
                is_active=True
            ).distinct()
        )

    async def get_ingredients(self, recipe_id: int) -> dict:
        ingredients = await sync_to_async(list)(
            Ingredient.objects.filter(recipe_id=recipe_id)
        )
        return {
            i.name: {"amount": i.amount, "unit": i.unit}
            for i in ingredients
        }

    async def get_steps(self, recipe_id: int) -> list:
        steps = await sync_to_async(list)(
            RecipeStep.objects.filter(recipe_id=recipe_id).order_by("order")
        )
        return steps

    async def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        return await sync_to_async(Recipe.objects.get)(id=recipe_id)

    async def save_dislike(self, user_id: int, recipe_id: int):
        user = await TelegramUser.objects.aget(telegram_id=user_id)
        await sync_to_async(user.disliked_recipes.add)(recipe_id)


recipe_service = RecipeService()
