from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import DietStates, BudgetStates

router = Router()

@router.callback_query(DietStates.waiting_for_diet_type, F.data.startswith("diet_"))
async def handle_diet_type(callback: CallbackQuery, state: FSMContext):
    diet_type = callback.data

    await state.update_data(diet=diet_type)

    await callback.message.answer(
        "💰 Введите ваш максимальный бюджет на блюдо (в рублях):"
    )
    await state.set_state(BudgetStates.waiting_for_budget)
