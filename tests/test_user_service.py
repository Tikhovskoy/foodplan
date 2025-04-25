import pytest
from unittest.mock import MagicMock
from bot.logic.user_service import UserService
from bot.logic.interfaces import UserPreferences
from bot.logic.exceptions import PreferenceError

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return UserService(prefs_repo=mock_repo)

def test_toggle_adds_category(service, mock_repo):
    prefs = UserPreferences(categories=[])
    mock_repo.get.return_value = prefs

    result = service.toggle(telegram_id=1, category="веган")

    assert "веган" in result.categories
    mock_repo.save.assert_called_once()

def test_toggle_removes_category(service, mock_repo):
    prefs = UserPreferences(categories=["веган"])
    mock_repo.get.return_value = prefs

    result = service.toggle(telegram_id=1, category="веган")

    assert "веган" not in result.categories
    mock_repo.save.assert_called_once()

def test_set_categories_valid(service, mock_repo):
    result = service.set_categories(telegram_id=1, new_categories=["веган", "без глютена"])
    assert result.categories == ["веган", "без глютена"]

def test_set_categories_invalid(service):
    with pytest.raises(PreferenceError):
        service.set_categories(telegram_id=1, new_categories=["веган", 123])
