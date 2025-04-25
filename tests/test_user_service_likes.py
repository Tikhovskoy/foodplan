import pytest
from users.models import User, Profile
from recipes.models import Recipe
from bot.logic.user_service import UserService
from bot.logic.exceptions import RecipeAlreadyLiked, RecipeAlreadyDisliked
from bot.logic.dto import UserPreferences
from bot.logic.interfaces import IUserPreferencesRepository

pytestmark = pytest.mark.django_db


class FakePreferencesRepo(IUserPreferencesRepository):
    def __init__(self):
        self.data = {}

    def get(self, telegram_id):
        return self.data.get(telegram_id, UserPreferences())

    def save(self, telegram_id, prefs):
        self.data[telegram_id] = prefs


@pytest.fixture
def prefs_repo():
    return FakePreferencesRepo()


@pytest.fixture
def test_user():
    user = User.objects.create(username="testuser", telegram_id=1)
    profile = Profile.objects.create(user=user)
    return profile


@pytest.fixture
def recipe():
    return Recipe.objects.create(title="Тестовый рецепт", estimated_cost=0)


@pytest.fixture
def service(prefs_repo):
    return UserService(prefs_repo=prefs_repo)


def test_like_recipe_adds_to_liked(service, test_user, recipe):
    result = service.like_recipe(telegram_id=1, recipe_id=recipe.id)
    assert recipe.id in result.liked_recipes
    assert recipe.id not in result.disliked_recipes


def test_like_recipe_twice_raises(service, test_user, recipe):
    service.like_recipe(telegram_id=1, recipe_id=recipe.id)
    with pytest.raises(RecipeAlreadyLiked):
        service.like_recipe(telegram_id=1, recipe_id=recipe.id)


def test_dislike_recipe_adds_to_disliked(service, test_user, recipe):
    result = service.dislike_recipe(telegram_id=1, recipe_id=recipe.id)
    assert recipe.id in result.disliked_recipes
    assert recipe.id not in result.liked_recipes


def test_dislike_recipe_twice_raises(service, test_user, recipe):
    service.dislike_recipe(telegram_id=1, recipe_id=recipe.id)
    with pytest.raises(RecipeAlreadyDisliked):
        service.dislike_recipe(telegram_id=1, recipe_id=recipe.id)


def test_dislike_removes_like(service, test_user, recipe):
    service.like_recipe(telegram_id=1, recipe_id=recipe.id)
    result = service.dislike_recipe(telegram_id=1, recipe_id=recipe.id)
    assert recipe.id in result.disliked_recipes
    assert recipe.id not in result.liked_recipes


def test_like_removes_dislike(service, test_user, recipe):
    service.dislike_recipe(telegram_id=1, recipe_id=recipe.id)
    result = service.like_recipe(telegram_id=1, recipe_id=recipe.id)
    assert recipe.id in result.liked_recipes
    assert recipe.id not in result.disliked_recipes
