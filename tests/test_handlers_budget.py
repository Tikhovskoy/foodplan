import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from decimal import Decimal
from bot.handlers.budget import handle_budget
from bot.states import BudgetStates
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
async def test_handle_budget_invalid_input():
    msg = DummyMessage("abc")
    state = DummyState()

    await handle_budget(message=msg, state=state)

    # При неверном вводе бот должен попросить ввести число
    assert "введите число" in msg.answers[-1].lower()

@pytest.mark.asyncio
async def test_handle_budget_valid_calls_send_recipes(monkeypatch):
    # Мокаем функцию send_recipes из модуля show_recipes
    import bot.handlers.show_recipes as sr_mod
    called = {}
    async def fake_send(msg, data):
        called['msg'] = msg
        called['data'] = data
    sr_mod.send_recipes = fake_send

    msg = DummyMessage("150")
    state = DummyState()

    await handle_budget(message=msg, state=state)

    # Проверяем, что budget сохранился и вызвался send_recipes
    assert called['msg'] is msg
    assert isinstance(called['data']['budget'], Decimal)
    assert called['data']['budget'] == Decimal("150")
