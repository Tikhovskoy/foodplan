from aiogram.fsm.state import State, StatesGroup

class RecipeStepStates(StatesGroup):
    waiting_for_like_or_dislike = State()
