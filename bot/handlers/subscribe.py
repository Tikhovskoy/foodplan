from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, PreCheckoutQuery, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from payments.models import SubscriptionPlan, Subscription, PaymentRecord

router = Router()
logger = logging.getLogger(__name__)


async def get_subscription_keyboard():
    plans = await SubscriptionPlan.objects.all().alist()

    builder = InlineKeyboardBuilder()
    for plan in plans:
        builder.add(InlineKeyboardButton(
            text=f"{plan.name} - {plan.price}₽",
            callback_data=f"subscribe_{plan.id}"
        ))

    builder.adjust(1)
    return builder.as_markup()


async def show_subscription_offer(message: types.Message):
    keyboard = await get_subscription_keyboard()
    await message.answer(
        "Для доступа к дополнительным функциям бота требуется подписка:\n"
        "Выберите подходящий вариант:",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("subscribe_"))
async def handle_subscription_selection(callback: types.CallbackQuery):
    plan_id = int(callback.data.split("_")[1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()

    if not plan:
        await callback.answer("Подписка не найдена", show_alert=True)
        return

    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Подписка {plan.name}",
        description=plan.description,
        payload=f"subscription_{plan.id}",
        provider_token="PAYMENT_TOKEN",    # Нужно будет вставить токен оплаты
        currency="RUB",
        prices=[LabeledPrice(label=plan.name, amount=int(plan.price * 100))],
        start_parameter="subscription"
    )
    await callback.answer()


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    if not payload.startswith("subscription_"):
        return

    plan_id = int(payload.split("_")[1])
    plan = await SubscriptionPlan.objects.filter(id=plan_id).afirst()

    user = await User.objects.aupdate_or_create(
        telegram_id=message.from_user.id,
        defaults={
            'username': message.from_user.username or f"tg_{message.from_user.id}",
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
        f"Подписка {plan.name} активирована до {subscription.end_date}!\n"
        f"Спасибо за доверие!"
    )
