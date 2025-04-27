from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import MealTypeStates, DietStates
from bot.keyboards.reply import get_diet_kb

router = Router()

@router.callback_query(MealTypeStates.waiting_for_meal_type, F.data.startswith("meal_"))
async def handle_meal_type(callback: CallbackQuery, state: FSMContext):
    meal_type = callback.data

    await state.update_data(meal_type=meal_type)

    await callback.message.answer(
        "🥗 Выберите тип диеты:",
        reply_markup=get_diet_kb()
    )
    await state.set_state(DietStates.waiting_for_diet_type)
