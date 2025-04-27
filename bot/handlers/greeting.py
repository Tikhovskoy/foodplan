from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from bot.states import SubscriptionStates, MealTypeStates
from bot.keyboards.reply import get_start_kb, get_subscription_kb, get_meal_type_kb
from bot.services.subscription_service import subscription_service
from bot.services.profile_service import profile_service

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        await message.answer(
            "👋 Добро пожаловать в FoodPlan!\n\n"
            "🚀 Нажмите кнопку ниже, чтобы начать!",
            reply_markup=get_start_kb()
        )
    except Exception as e:
        print(f"Error in cmd_start: {e}")
        await message.answer("⚠️ Произошла ошибка при запуске бота.")

@router.callback_query(F.data == "start")
async def on_start_button(callback: CallbackQuery, state: FSMContext):
    try:
        await start_flow(callback.message, state)
        await callback.answer()
    except Exception as e:
        print(f"Error in on_start_button: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при запуске.")
        await callback.answer()

@router.chat_member()
async def on_user_join(event: ChatMemberUpdated, state: FSMContext):
    try:
        if event.new_chat_member.status == "member":
            await event.chat.send_message(
                "👋 Добро пожаловать в FoodPlan!\n\n"
                "🚀 Нажмите кнопку ниже, чтобы начать!",
                reply_markup=get_start_kb()
            )
    except Exception as e:
        print(f"Error in on_user_join: {e}")

async def start_flow(chat_or_message, state: FSMContext):
    try:
        await state.clear()
        user_id = chat_or_message.from_user.id if hasattr(chat_or_message, 'from_user') else chat_or_message.id

        await profile_service.get_or_create_profile(user_id)
        is_active = await subscription_service.check_active(user_id)

        if is_active:
            await chat_or_message.answer(
                "🍽 Выберите тип питания:",
                reply_markup=get_meal_type_kb()
            )
            await state.set_state(MealTypeStates.waiting_for_meal_type)
        else:
            await chat_or_message.answer(
                "🔒 Хотите оформить подписку?",
                reply_markup=get_subscription_kb()
            )
            await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    except Exception as e:
        print(f"Error in start_flow: {e}")
        await chat_or_message.answer("⚠️ Ошибка при запуске, попробуйте позже.")