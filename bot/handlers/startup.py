from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.services.subscription_service import subscription_service
from bot.states import SubscriptionStates, MealTypeStates
from bot.keyboards.reply import get_meal_type_kb, get_subscription_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await start_flow(message, state)

@router.chat_member()
async def on_user_join(event: ChatMemberUpdated, state: FSMContext):
    if event.new_chat_member.status == "member":
        await start_flow(event.chat, state)

async def start_flow(chat_or_message, state: FSMContext):
    await state.clear()
    user_id = chat_or_message.from_user.id if hasattr(chat_or_message, "from_user") else chat_or_message.id

    try:
        is_active = await subscription_service.check_active(user_id)

        if is_active:
            await chat_or_message.answer(
                "🍽 Выберите тип питания:",
                reply_markup=get_meal_type_kb()
            )
            await state.set_state(MealTypeStates.waiting_for_meal_type)
        else:
            await chat_or_message.answer(
                "🔒 Для использования бота нужна подписка.\nХотите оформить подписку?",
                reply_markup=get_subscription_kb()
            )
            await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    except Exception as e:
        await chat_or_message.answer("⚠️ Ошибка при проверке подписки. Попробуйте позже.")
        print(f"Ошибка в start_flow: {e}")
