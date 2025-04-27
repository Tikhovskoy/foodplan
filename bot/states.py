from aiogram.fsm.state import StatesGroup, State

class SubscriptionStates(StatesGroup):
    """Состояния для проверки подписки"""
    waiting_for_subscription_choice = State()

class MealTypeStates(StatesGroup):
    """Состояния для выбора типа питания"""
    waiting_for_meal_type = State()

class DietStates(StatesGroup):
    """Состояния для выбора типа диеты"""
    waiting_for_diet_type = State()

class BudgetStates(StatesGroup):
    """Состояния для ввода бюджета"""
    waiting_for_budget = State()

class RecipeStepStates(StatesGroup):
    showing_step = State()
