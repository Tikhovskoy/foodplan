from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import CategoryState
from bot.keyboards.reply import get_categories_kb
from bot.keyboards.reply import get_meal_type_kb


router = Router()

@router.callback_query(F.data.startswith("meal_"))
async def handle_meal_time(callback: CallbackQuery, state: FSMContext):
    meal_id = int(callback.data.replace("meal_", ""))
    await state.update_data(meal_time_id=meal_id)

    await callback.message.edit_text(
        "🍽 Отлично! Теперь выберите предпочтительную категорию:",
        reply_markup=await get_categories_kb()
    )
    await state.set_state(CategoryState.select_category)

@router.callback_query(F.data == "back_to_meal_types")
async def back_to_meal_types(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "🍽 Выберите время приёма пищи:",
        reply_markup=await get_meal_type_kb()
    )