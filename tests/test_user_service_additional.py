import pytest
from unittest.mock import MagicMock
from bot.logic.user_service import UserService
from bot.logic.interfaces import UserPreferences


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return UserService(prefs_repo=mock_repo)


def test_get_preferences(service, mock_repo):
    prefs = UserPreferences(categories=["веган"])
    mock_repo.get.return_value = prefs

    result = service.get_preferences(telegram_id=1)

    assert result.categories == ["веган"]
    mock_repo.get.assert_called_once_with(telegram_id=1)


def test_has_category_true(service, mock_repo):
    prefs = UserPreferences(categories=["веган"])
    mock_repo.get.return_value = prefs

    assert service.has_category(telegram_id=1, category="веган") is True


def test_has_category_false(service, mock_repo):
    prefs = UserPreferences(categories=["без глютена"])
    mock_repo.get.return_value = prefs

    assert service.has_category(telegram_id=1, category="веган") is False
