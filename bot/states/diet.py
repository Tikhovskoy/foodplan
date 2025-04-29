from aiogram.fsm.state import StatesGroup, State

class DietStates(StatesGroup):
    waiting_for_diet_type = State()
