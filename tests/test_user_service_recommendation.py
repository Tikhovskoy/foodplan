import pytest
from recipes.models import Recipe
from users.models import Category
from users.models import TelegramUser, Profile
from bot.logic.user_service import UserService
from bot.adapters.user_repository import DjangoUserPreferencesRepository

@pytest.mark.django_db
def test_recommend_recipe_returns_valid_recipe():
    # Пользователь и профиль
    user = User.objects.create(username="recommender", telegram_id=999)
    profile = Profile.objects.create(user=user)


    # Категории
    vegan = Category.objects.create(name="Веган")
    keto = Category.objects.create(name="Кето")
    profile.categories.add(vegan, keto)

    # Подходящий рецепт
    good_recipe = Recipe.objects.create(title="Веган-салат", estimated_cost=100)
    good_recipe.categories.add(vegan)

    # Дизлайкнутый рецепт
    bad_recipe = Recipe.objects.create(title="Мясо с кетчупом", estimated_cost=200)
    bad_recipe.categories.add(keto)
    profile.disliked.add(bad_recipe)

    profile.save()

    # Тест логики
    service = UserService(DjangoUserPreferencesRepository())
    recommended = service.recommend_recipe(telegram_id=999)

    assert recommended is not None
    assert recommended == good_recipe
