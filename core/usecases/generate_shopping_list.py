from recipes.services import RecipeRepository

class GenerateShoppingListUseCase:
    """
    Use-case: сгенерировать список покупок по ID рецепта.
    """
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    def execute(self, recipe_id: int) -> dict:
        recipe = self.recipe_repo.get_by_id(recipe_id)
        lines, total = recipe.get_shopping_lines()
        return {
            "recipe_title": recipe.title,
            "lines": lines,
            "total": total,
        }
