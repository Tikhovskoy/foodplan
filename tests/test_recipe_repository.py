import pytest
from recipes.models import Recipe
from bot.adapters.recipe_repository import DjangoRecipeRepository
from bot.logic.exceptions import RecipeNotFound

@pytest.mark.django_db
def test_list_active_recipes():
    Recipe.objects.create(title="Тестовый", is_active=True)
    repo = DjangoRecipeRepository()
    recipes = repo.list_active()
    assert len(recipes) == 1
    assert recipes[0].title == "Тестовый"

@pytest.mark.django_db
def test_list_active_recipes_empty():
    repo = DjangoRecipeRepository()
    with pytest.raises(RecipeNotFound):
        repo.list_active()
