from aiogram.fsm.state import State, StatesGroup

class SubscriptionStates(StatesGroup):
    waiting_for_subscription_choice = State()
