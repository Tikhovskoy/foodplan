from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import get_subscription_kb, get_meal_type_kb
from bot.states import MealTypeStates
from bot.shared.send_tools import send_recipe
from users.models import TelegramUser
from recipes.models import Recipe
from random import choice
from asgiref.sync import sync_to_async
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username or f"tg_{message.from_user.id}",
            "first_name": message.from_user.first_name or "",
            "last_name": message.from_user.last_name or ""
        }
    )

    if user.has_active_subscription():
        meal_type_kb = await get_meal_type_kb()
        await message.answer(
            "🍽 Выберите время приёма пищи:",
            reply_markup=meal_type_kb
        )
        await state.set_state(MealTypeStates.waiting_for_meal_type)
    else:
        buttons = [
            ("💳 Оформить подписку", "buy_subscription"),
            ("🍽 Получить бесплатный рецепт", "get_free_recipe"),
        ]
        await message.answer(
            "🔒 У вас нет активной подписки. Вы можете оформить подписку или получить бесплатный рецепт:",
            reply_markup=get_subscription_kb(buttons)
        )

@router.callback_query(F.data == "get_free_recipe")
async def get_free_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(telegram_id=callback.from_user.id)

        if not user.can_get_free_recipe():
            await callback.message.answer("⚠️ Сегодня вы уже получили бесплатный рецепт. Приходите завтра!")
            await callback.answer()
            return

        recipes = await sync_to_async(list)(Recipe.objects.filter(is_active=True))

        if not recipes:
            await callback.message.answer("⚠️ Рецепты пока отсутствуют. Попробуйте позже.")
            await callback.answer()
            return

        recipe = choice(recipes)

        caption = f"🍽 Ваш рецепт:\n\n📓 {recipe.title}\n\n📝 {recipe.description}"
        await send_recipe(
            callback.message,
            caption=caption,
            image_field=recipe.image,
            reply_markup=None
        )

        user.last_free_recipe = timezone.now().date()
        await sync_to_async(user.save)()

        await state.clear()

        await callback.message.answer(
            "🚀 Для полного доступа ко всем рецептам, диетам и функциям бота оформите подписку!",
            reply_markup=get_subscription_kb([
                ("💳 Оформить подписку", "buy_subscription"),
            ])
        )

        await callback.answer()

    except Exception as e:
        logger.exception("Ошибка при выдаче бесплатного рецепта")
        await callback.message.answer("⚠️ Произошла ошибка при получении бесплатного рецепта.")
