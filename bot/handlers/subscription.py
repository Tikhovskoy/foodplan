import yookassa
from aiogram import Router, types, F
from aiogram.types import PreCheckoutQuery
from payments.models import SubscriptionPlan, Subscription, PaymentRecord
from users.models import TelegramUser
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()

SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

yookassa.Configuration.account_id = SHOP_ID
yookassa.Configuration.secret_key = SECRET_KEY

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data.startswith("subscribe_"))
async def handle_subscription_selection(callback: types.CallbackQuery):
    plan_id = int(callback.data.split("_")[1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()

    if not plan:
        await callback.answer("Подписка не найдена", show_alert=True)
        return

    user_id = callback.from_user.id
    user = await TelegramUser.objects.filter(telegram_id=user_id).afirst()

    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    has_active_subscription = await Subscription.objects.filter(
        user=user,
        end_date__gte=datetime.now()
    ).aexists()

    if has_active_subscription:
        await callback.message.answer("✅ Ваша подписка уже активна.")
    else:
        payment = yookassa.Payment.create(
            amount={"value": str(plan.price), "currency": "RUB"},
            capture=True,
            description=f"Подписка на {plan.name}",
            metadata={"user_id": user_id, "plan_id": plan.id},
            confirmation={"type": "redirect", "return_url": "https://t.me/your_bot"},
            receipt={
                "items": [
                    {
                        "description": plan.name,
                        "quantity": "1",
                        "amount": {"value": str(plan.price), "currency": "RUB"},
                        "vat_code": 1,
                    }
                ]
            }
        )

        payment_url = payment.confirmation.confirmation_url
        await callback.bot.send_message(
            callback.message.chat.id,
            f"Перейдите по ссылке для оплаты подписки: {payment_url}",
        )
        await callback.answer()

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload

    if not payload.startswith("subscription_"):
        return

    plan_id = int(payload.split("_")[1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()

    if not plan:
        await message.answer("Ошибка: План подписки не найден.")
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
        amount=message.successful_payment.total_amount / 100
    )

    await PaymentRecord.objects.acreate(
        subscription=subscription,
        telegram_payment_id=message.successful_payment.telegram_payment_charge_id,
        status="completed"
    )

    await message.answer(
        f"Подписка на {plan.name} активирована!\n"
        f"Спасибо за доверие!"
    )

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
