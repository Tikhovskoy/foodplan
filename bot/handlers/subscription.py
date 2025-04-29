import os
from datetime import date, timedelta
from dotenv import load_dotenv

from aiogram import Router, types, F, Bot
from aiogram.types import (
    LabeledPrice,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    PreCheckoutQuery,
)
from asgiref.sync import sync_to_async

from payments.models import SubscriptionPlan, Subscription, PaymentRecord
from users.models import TelegramUser
from bot.keyboards.reply import get_meal_type_kb

load_dotenv()
router = Router()
PAYMENT_TOKEN = os.getenv("TELEGRAM_PAYMENT_TOKEN")


@router.callback_query(F.data == "buy_subscription")
async def handle_buy_subscription(callback: types.CallbackQuery):
    await callback.answer()
    plans = await sync_to_async(list)(SubscriptionPlan.objects.all())

    if not plans:
        await callback.message.answer("Тарифы пока не настроены.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=plan.name, callback_data=f"pay_plan_{plan.id}")]
        for plan in plans
    ])

    await callback.message.answer("💳 Выберите тариф для оплаты:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("pay_plan_"))
async def handle_pay_plan(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()
    plan_id = int(callback.data.split("_")[-1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()

    if not plan:
        await callback.message.answer("Ошибка: тариф не найден.")
        return

    prices = [LabeledPrice(label=plan.name, amount=int(plan.price * 100))]

    payload = f"subscription_{plan.id}"
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Подписка {plan.name}",
        description=plan.description or f"Подписка на {plan.name}",
        payload=payload,
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="foodplan-payment"
    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout: PreCheckoutQuery):
    await pre_checkout.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    if not payload.startswith("subscription_"):
        return

    plan_id = int(payload.split("_")[1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()
    if not plan:
        await message.answer("Ошибка: тариф не найден.")
        return

    user, _ = await TelegramUser.objects.aget_or_create(
        telegram_id=message.from_user.id,
        defaults={
            'username': message.from_user.username or f"user_{message.from_user.id}",
            'first_name': message.from_user.first_name or "",
            'last_name': message.from_user.last_name or ""
        }
    )

    subscription = await Subscription.objects.acreate(
        user=user,
        plan=plan,
        amount=plan.price,
        end_date=date.today() + timedelta(days=plan.duration)
    )

    await PaymentRecord.objects.acreate(
        subscription=subscription,
        telegram_payment_id=message.successful_payment.telegram_payment_charge_id,
        status="completed"
    )

    await message.answer(
        f"✅ Подписка на {plan.name} активирована. Приятного использования!"
    )

    keyboard = await get_meal_type_kb()
    await message.answer(
        "🍽 Выберите время приёма пищи:",
        reply_markup=keyboard
)
