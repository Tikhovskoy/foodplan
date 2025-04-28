from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from recipes.models import Recipe
import random
import os
from aiogram import types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Рецепт дня", callback_data='recipe')],
            [
                InlineKeyboardButton(text="❤️ Избранное", callback_data='favorite'),
                InlineKeyboardButton(text="⚙️ Настройки", callback_data='setting_order')
            ],
        ]
    )
    await message.answer(
        "Привет 👋\n"
        "Я помогу тебе с рецептами на каждый день!\n\n"
        "🔹 Хочешь получить рецепт дня?\n"
        "🔹 Нужен список покупок?\n"
        "🔹 Или хочешь указать предпочтения (веган, без глютена)?\n\n"
        "Выбирай команду ниже или жми кнопку меню!",
        reply_markup=keyboard
    )


@sync_to_async
def get_random_recipe_data():
    recipes = list(Recipe.objects.filter(is_active=True))
    if not recipes:
        return None

    recipe = random.choice(recipes)

    ingredients = [
        f"{ri.ingredient.name} — {ri.amount} {ri.get_unit_display()}"
        for ri in recipe.recipeingredient_set.all()
    ]

    steps = [
        f"{s.order}. {s.text}"
        for s in recipe.steps.all().order_by("order")
    ]

    return {
        "title": recipe.title,
        "ingredients": ingredients,
        "steps": steps,
        "image": FSInputFile(recipe.image.path) if recipe.image else None,
        "step_images": [
            FSInputFile(s.image.path) if s.image else None
            for s in recipe.steps.all().order_by("order")
        ],
        "price": recipe.estimated_cost,
    }


@router.callback_query(lambda c: c.data == "recipe")
async def get_recipe(callback: types.CallbackQuery):
    await callback.answer()

    # Получаем данные о рецепте
    recipe_data = await get_random_recipe_data()


    if recipe_data:
        ingredients = "\n".join(recipe_data['ingredients'])
        # Формируем сообщение с рецептом
        message = f"🍽️ Рецепт дня: {recipe_data['title']}\n\n{ingredients}"


        # Добавляем изображение блюда, если оно есть
        if recipe_data['image']:
            await callback.message.answer_photo(
                photo=recipe_data['image'],
                caption=message
            )
        else:
            await callback.message.answer(message)  # Если изображения нет, просто отправляем сообщение

        # Ингредиенты
        # ingredients_message = "🛒 Ингредиенты:\n" + "\n".join(recipe_data['ingredients'])
        # await callback.message.answer(ingredients_message)

        # Шаги приготовления
        for step, step_image_url in zip(recipe_data['steps'], recipe_data['step_images']):
            step_message = f"{step}\n"
            if step_image_url:
                # Отправляем изображение для шага, если оно есть
                await callback.message.answer_photo(photo=step_image_url, caption=step_message)
            else:
                # Если изображения шага нет, отправляем только текст шага
                await callback.message.answer(step_message)


    else:
        await callback.message.edit_text("Извините, рецепты сейчас недоступны.")

    price = f'Общая стоимость блюда {recipe_data["price"]} руб.'
    await callback.message.answer(price)