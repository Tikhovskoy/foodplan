from asgiref.sync import sync_to_async
from recipes.models import Recipe
from bot.logic.exceptions import RecipeNotFound

class DjangoRecipeRepository:
    @sync_to_async
    def list_active(self):
        recipes = Recipe.objects.filter(is_active=True)
        if not recipes.exists():
            raise RecipeNotFound("Нет доступных рецептов")
        return list(recipes)

    @sync_to_async
    def get(self, recipe_id: int):
        try:
            return Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise RecipeNotFound("Рецепт не найден.")
