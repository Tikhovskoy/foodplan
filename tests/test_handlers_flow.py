import sys, os
# Убедимся, что корень проекта (где лежит папка bot/) в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import AsyncMock, MagicMock

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Импортируем именно из greeting.py
from bot.handlers.greeting import cmd_start
from bot.states import SubscriptionStates, MealTypeStates

class DummyMessage:
    def __init__(self, user_id):
        self.from_user = MagicMock(id=user_id)
        self.answers = []
        self.answer = AsyncMock(side_effect=lambda text: self.answers.append(text))

class DummyState:
    def __init__(self):
        self._state = None
    async def set_state(self, state):
        self._state = state
    async def clear(self):
        self._state = None

@pytest.mark.asyncio
async def test_start_no_subscription():
    # Мокаем subscription_service.check_active → False
    import bot.handlers.greeting as start_mod
    start_mod.subscription_service.check_active = lambda tid: False

    msg = DummyMessage(user_id=42)
    state = DummyState()
    await cmd_start(msg, state)

    # Проверяем ответы и состояние
    assert any("нет подписки" in ans for ans in msg.answers), msg.answers
    assert state._state == SubscriptionStates.waiting_for_subscription_choice

@pytest.mark.asyncio
async def test_start_with_subscription():
    # Мокаем subscription_service.check_active → True
    import bot.handlers.greeting as start_mod
    start_mod.subscription_service.check_active = lambda tid: True

    msg = DummyMessage(user_id=99)
    state = DummyState()
    await cmd_start(msg, state)

    assert any("активная подписка" in ans for ans in msg.answers), msg.answers
    assert state._state == MealTypeStates.waiting_for_meal_type
