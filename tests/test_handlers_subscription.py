import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import AsyncMock, MagicMock

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.handlers.subscription import subscribe_yes, subscribe_no
from bot.states import SubscriptionStates, MealTypeStates

class DummyMessage:
    def __init__(self, user_id, text=""):
        self.from_user = type("U", (), {"id": user_id})
        self.text = text
        self.answers = []
        self.answer = AsyncMock(side_effect=lambda text, **kwargs: self.answers.append(text))

class DummyState:
    def __init__(self):
        self._state = None
    
    async def set_state(self, state):
        self._state = state
    
    async def clear(self):
        self._state = None
    
    async def get_state(self):
        return self._state

@pytest.mark.asyncio
async def test_subscribe_yes(monkeypatch):
    import bot.handlers.subscription as sub_mod
    
    # Mock subscription service
    called = {}
    def fake_extend(tid, days):
        called["tid"] = tid
        called["days"] = days
    
    sub_mod.subscription_service = MagicMock()
    sub_mod.subscription_service.extend = fake_extend

    msg = DummyMessage(user_id=7, text="Да")
    state = DummyState()
    await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    
    await subscribe_yes(msg, state)

    assert called == {"tid": 7, "days": 30}
    assert state._state == MealTypeStates.waiting_for_meal_type
    assert any("Подписка оформлена на 30 дней" in ans for ans in msg.answers)

@pytest.mark.asyncio
async def test_subscribe_no(monkeypatch):
    import bot.handlers.subscription as sub_mod

    class FakeRecipe:
        title = "Test Recipe"
        description = "Test Description"
    
    # Mock all dependencies
    sub_mod.RecipeService = MagicMock()
    sub_mod.RecipeService.return_value.fetch_random.return_value = FakeRecipe()
    sub_mod.DjangoRecipeRepository = lambda: None
    sub_mod.DjangoFeedbackRepository = lambda: None
    sub_mod.DjangoUserPreferencesRepository = lambda: None

    msg = DummyMessage(user_id=8, text="Нет")
    state = DummyState()
    await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    
    await subscribe_no(msg, state)

    assert any("<b>Test Recipe</b>" in ans for ans in msg.answers)
    assert any("Test Description" in ans for ans in msg.answers)
    assert state._state is None