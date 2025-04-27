from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import SubscriptionStates, MealTypeStates
from bot.keyboards.reply import get_meal_type_kb, get_buy_subscription_kb
from bot.services.subscription_service import subscription_service
from bot.logic.exceptions import SubscriptionError

router = Router()

@router.callback_query(SubscriptionStates.waiting_for_subscription_choice, F.data.in_(["subscribe_yes", "subscribe_no"]))
async def handle_subscription_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data == "subscribe_yes":
        try:
            await subscription_service.extend_subscription(callback.from_user.id, days=30)
            await callback.message.answer(
                "✅ Подписка успешно оформлена!\n\n🍽 Выберите тип питания:",
                reply_markup=get_meal_type_kb()
            )
            await state.set_state(MealTypeStates.waiting_for_meal_type)
        except SubscriptionError as e:
            await callback.message.answer(f"⚠️ Ошибка оформления подписки: {e}")
            await state.clear()
    else:
        await callback.message.answer("🚫 Вы отказались от подписки. Один рецепт доступен в день.")
        await state.clear()

@router.callback_query(SubscriptionStates.waiting_for_subscription_choice, F.data.in_(["buy_subscription", "decline_subscription"]))
async def handle_buy_subscription_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data == "buy_subscription":
        try:
            await subscription_service.extend_subscription(callback.from_user.id, days=30)
            from bot.handlers.greeting import start_flow
            await callback.message.answer("✅ Подписка успешно оформлена! 🎉")
            await start_flow(callback.message, state)
        except Exception as e:
            await callback.message.answer(f"⚠️ Ошибка оформления подписки: {e}")
            await state.clear()
    else:
        await callback.message.answer("🚫 Вы отказались от подписки. Один рецепт доступен в день.")
        await state.clear()
