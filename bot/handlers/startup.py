from aiogram import Router, types
from aiogram.filters import CommandStart
from users.models import TelegramUser
from payments.models import Subscription
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        user, created = await TelegramUser.objects.aget_or_create(
            telegram_id=message.from_user.id,
            defaults={
                'username': message.from_user.username or f"user_{message.from_user.id}",
                'first_name': message.from_user.first_name or "",
                'last_name': message.from_user.last_name or ""
            }
        )
        if created:
            logger.info(f"Создан новый пользователь: {user.telegram_id}")
        else:
            logger.info(f"Пользователь уже существует: {user.telegram_id}")

    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {e}")
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")
        return

    # Проверяем активную подписку
    has_active_subscription = await Subscription.objects.filter(
        user=user,
        end_date__gte=datetime.now()
    ).aexists()

    if has_active_subscription:
        await message.answer("✅ Ваша подписка активна. Выберите категорию питания!")
    else:
        await message.answer("❗ Чтобы пользоваться всеми функциями, пожалуйста, оформите подписку.")
