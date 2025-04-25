import pytest
from users.models import User, Profile
from recipes.models import Recipe
from bot.adapters.feedback_repository import DjangoFeedbackRepository

@pytest.mark.django_db
def test_save_and_list_disliked():
    user = User.objects.create(username="test", telegram_id=555)
    profile = Profile.objects.create(user=user)
    recipe = Recipe.objects.create(title="Test", is_active=True)

    repo = DjangoFeedbackRepository()
    repo.save_feedback(telegram_id=555, recipe_id=recipe.id, kind="dislike")

    disliked = repo.list_disliked(telegram_id=555)
    assert recipe.id in disliked
