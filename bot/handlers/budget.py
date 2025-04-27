from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from bot.states import BudgetStates
from bot.handlers.show_recipes import send_recipes

router = Router()

@router.message(BudgetStates.waiting_for_budget)
async def handle_budget(message: Message, state: FSMContext):
    try:
        budget = Decimal(message.text)
        if budget <= 0:
            raise ValueError
    except (ValueError, InvalidOperation):
        await message.answer("⚠️ Введите корректную сумму (например: 200)")
        return

    await state.update_data(budget=str(budget))

    await send_recipes(message, state)
    await state.clear()
