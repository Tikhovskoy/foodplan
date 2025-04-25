import pytest
from django.contrib.auth import get_user_model
from users.models import Profile, Category
from bot.adapters.user_repository import DjangoUserPreferencesRepository

User = get_user_model()

@pytest.mark.django_db
def test_get_and_save_preferences():
    # Arrange
    user = User.objects.create(username="tester", telegram_id=123)
    profile = Profile.objects.create(user=user)
    vegan = Category.objects.create(name="веган")
    gluten = Category.objects.create(name="без глютена")

    repo = DjangoUserPreferencesRepository()

    # Act — получить начальные настройки
    prefs = repo.get(telegram_id=123)
    assert prefs.categories == []

    # Сохраняем новые категории
    prefs.categories = ["веган", "без глютена"]
    repo.save(telegram_id=123, prefs=prefs)

    # Проверяем, что сохранилось
    updated = repo.get(telegram_id=123)
    assert "веган" in updated.categories
    assert "без глютена" in updated.categories
