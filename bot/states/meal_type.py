from aiogram.fsm.state import StatesGroup, State

class MealTypeStates(StatesGroup):
    waiting_for_meal_type = State()
