from typing import List
from recipes.models import Recipe
from bot.logic.exceptions import RecipeNotFound
from bot.logic.interfaces import IRecipeRepository

class DjangoRecipeRepository(IRecipeRepository):
    def list_active(self) -> List[Recipe]:
        recipes = Recipe.objects.filter(is_active=True)
        if not recipes.exists():
            raise RecipeNotFound("Нет доступных рецептов")
        return list(recipes)
