import pytest
from unittest.mock import AsyncMock

class DummyMessage:
    def __init__(self, text):
        self.text = text  # Текст сообщения ("веган")
        self.answer = AsyncMock()  # Делаем answer асинхронным!
        # Чтобы проверить, что бот ответил:
        self.answer.side_effect = lambda reply_text: setattr(self, "last_reply", reply_text)

class DummyState:
    def __init__(self):
        self._data = {}  # Здесь сохраняются данные
        self._state = None  # Здесь хранится следующее состояние
    
    async def update_data(self, **kwargs):
        self._data.update(kwargs)  # Сохраняем данные (например, diet="веган")
    
    async def set_state(self, state):
        self._state = state  # Запоминаем новое состояние

@pytest.mark.asyncio
async def test_handle_diet_sets_data_and_next_state():
    # 1. Подготовка
    msg = DummyMessage("веган")  # Пользователь написал "веган"
    state = DummyState()  # Создаём "чистое" состояние
    
    # 2. Вызов обработчика
    from bot.handlers.diet import handle_diet
    await handle_diet(message=msg, state=state)
    
    # 3. Проверки
    assert state._data == {"diet": "веган"}  # Данные сохранились?
    assert "бюджет" in msg.last_reply.lower()  # Бот спросил про бюджет?
    assert state._state == "BudgetStates:waiting_for_budget"  # Состояние изменилось?