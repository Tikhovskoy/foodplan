import pytest
from recipes.models import Recipe
from users.models import TelegramUser, Profile, Category
from bot.logic.user_service import UserService
from bot.adapters.user_repository import DjangoUserPreferencesRepository

@pytest.mark.django_db
def test_skip_recipe_returns_different_recipe():
    user = User.objects.create(username="skipper", telegram_id=555)
    profile = Profile.objects.create(user=user)

    cat = Category.objects.create(name="Фрукты")
    profile.categories.add(cat)

    r1 = Recipe.objects.create(title="Яблочный пирог", estimated_cost=100)
    r2 = Recipe.objects.create(title="Грушевый смузи", estimated_cost=80)
    r3 = Recipe.objects.create(title="Банановый кекс", estimated_cost=90)

    for r in [r1, r2, r3]:
        r.categories.add(cat)

    profile.save()

    service = UserService(DjangoUserPreferencesRepository())
    skipped = service.skip_recipe(telegram_id=555, current_recipe_id=r1.id)

    assert skipped is not None
    assert skipped.id != r1.id
