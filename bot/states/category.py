from aiogram.fsm.state import StatesGroup, State

class CategoryState(StatesGroup):
    select_category = State()
