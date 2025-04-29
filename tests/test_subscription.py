import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.services.subscription_service import subscription_service
from bot.logic.exceptions import RecipeNotFound
from bot.keyboards.reply import get_buy_subscription_kb
from bot.handlers.show_recipes import next_recipe
from aiogram.fsm.context import FSMContext


@pytest.mark.asyncio
async def test_next_recipe_with_active_subscription(mock_callback, mock_fsm):
    """
    Тестируем сценарий с активной подпиской:
    Метод send_recipes должен быть вызван, так как подписка активна.
    """
    # Мокируем проверку подписки
    subscription_service.check_active = AsyncMock(return_value=True)  # Подписка активна

    # Мокируем вызов send_recipes
    mock_send_recipes = AsyncMock()
    subscription_service.send_recipes = mock_send_recipes  # Подменяем send_recipes на мок

    # Вызываем next_recipe
    await next_recipe(mock_callback, mock_fsm)

    # Проверяем, что метод send_recipes был вызван
    mock_send_recipes.assert_called_once()  # Проверка, что send_recipes был вызван

@pytest.mark.asyncio
async def test_next_recipe_without_subscription(mock_callback, mock_fsm):
    """
    Тестируем сценарий с неактивной подпиской:
    Метод answer должен быть вызван с текстом и кнопками для оформления подписки.
    """
    # Мокируем проверку подписки
    subscription_service.check_active = AsyncMock(return_value=False)  # Подписка неактивна

    # Мокируем вызов метода answer для отправки сообщения
    mock_send_subscription_message = AsyncMock()
    mock_callback.message.answer = mock_send_subscription_message  # Мокаем answer

    # Вызываем next_recipe
    await next_recipe(mock_callback, mock_fsm)

    # Проверяем, что метод answer был вызван с правильным текстом и кнопками
    mock_send_subscription_message.assert_called_with(
        mock_callback.message,
        "🔒 Для просмотра дополнительных рецептов требуется подписка.\nХотите оформить подписку?",
        reply_markup=get_buy_subscription_kb()
    )


# Фикстуры для мокирования
@pytest.fixture
def mock_callback():
    """Мокируем callback_query (например, для вызова функции next_recipe)"""
    mock = MagicMock()
    mock.message = MagicMock()
    mock.message.answer = AsyncMock()
    return mock


@pytest.fixture
def mock_fsm():
    """Мокируем FSMContext, если он нужен"""
    return MagicMock(spec=FSMContext)
