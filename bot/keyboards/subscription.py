from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from payments.models import SubscriptionPlan
import logging

logger = logging.getLogger(__name__)

async def get_subscription_kb() -> InlineKeyboardMarkup:
    """
    Генерация клавиатуры с кнопками подписок из модели SubscriptionPlan.
    Если подписок нет, выводится сообщение об отсутствии доступных подписок.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)

    try:
        plans = await SubscriptionPlan.objects.all()
        
        if not plans:
            # Если нет ни одной подписки
            keyboard.add(
                InlineKeyboardButton(
                    text="Нет доступных подписок",
                    callback_data="no_subscriptions"
                )
            )
            return keyboard

        for plan in plans:
            button_text = f"{plan.name} - {plan.price}₽"
            callback_data = f"subscribe_{plan.id}"
            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    except Exception as e:
        logger.exception("Ошибка при получении подписок из базы данных")
        keyboard.add(
            InlineKeyboardButton(
                text="Ошибка загрузки подписок",
                callback_data="subscription_error"
            )
        )

    return keyboard
