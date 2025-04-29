from aiogram.fsm.state import StatesGroup, State

class BudgetStates(StatesGroup):
    waiting_for_budget = State()
