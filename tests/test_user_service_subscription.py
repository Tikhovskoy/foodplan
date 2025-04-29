import pytest
from datetime import timedelta
from django.utils import timezone

from users.models import TelegramUser, Profile, Category
from recipes.models import Recipe
from bot.logic.user_service import UserService
from bot.adapters.user_repository import DjangoUserPreferencesRepository

pytestmark = pytest.mark.django_db


def create_test_recipe(title, category):
    recipe = Recipe.objects.create(title=title, estimated_cost=100)
    recipe.categories.add(category)
    return recipe


def test_user_without_subscription_gets_one_recipe_per_day():
    user = User.objects.create(username="no_sub_user", telegram_id=1001)
    profile = Profile.objects.create(user=user)
    category = Category.objects.create(name="Овощи")
    profile.categories.add(category)

    recipe = create_test_recipe("Овощной суп", category)

    service = UserService(DjangoUserPreferencesRepository())

    # Первый рецепт должен быть выдан
    result_1 = service.get_daily_recipe(user.telegram_id)
    assert result_1 == recipe

    # Второй — уже нет
    result_2 = service.get_daily_recipe(user.telegram_id)
    assert result_2 is None


def test_user_with_subscription_gets_unlimited_recipes():
    user = User.objects.create(username="sub_user", telegram_id=1002)
    profile = Profile.objects.create(user=user)
    profile.paid_until = timezone.now().date() + timedelta(days=1)
    profile.save()

    category = Category.objects.create(name="Фрукты")
    profile.categories.add(category)

    recipe_1 = create_test_recipe("Фруктовый салат", category)
    recipe_2 = create_test_recipe("Фруктовый микс", category)

    service = UserService(DjangoUserPreferencesRepository())

    # Без ограничения
    result_1 = service.get_daily_recipe(user.telegram_id)
    result_2 = service.get_daily_recipe(user.telegram_id)

    assert result_1 in [recipe_1, recipe_2]
    assert result_2 in [recipe_1, recipe_2]


def test_user_without_suitable_recipes_gets_none():
    user = User.objects.create(username="empty_user", telegram_id=1003)
    Profile.objects.create(user=user)

    service = UserService(DjangoUserPreferencesRepository())

    result = service.get_daily_recipe(user.telegram_id)
    assert result is None
