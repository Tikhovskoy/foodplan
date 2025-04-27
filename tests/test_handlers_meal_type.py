import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from bot.handlers.meal_type import handle_meal_type
from bot.states import MealTypeStates, DietStates
from aiogram.types import Message

class DummyMessage:
    def __init__(self, text):
        self.text = text
        self.answers = []
        self.answer = lambda msg: self.answers.append(msg)
        self.from_user = type("U", (), {"id": 1})

class DummyState:
    def __init__(self):
        self._state = None
        self._data = {}
    async def set_state(self, state):
        self._state = state
    async def update_data(self, **kw):
        self._data.update(kw)
    async def get_data(self):
        return self._data

@pytest.mark.asyncio
async def test_handle_meal_type_sets_data_and_next_state():
    msg = DummyMessage("завтрак")
    state = DummyState()

    await handle_meal_type(message=msg, state=state)

    assert state._data["meal_type"] == "завтрак"
    assert state._state == DietStates.waiting_for_diet
