from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from recipes.models import Category, MealTime

def get_main_menu_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="🍽 Получить рецепт", callback_data="get_recipe")],
        [
            InlineKeyboardButton(text="📖 Мои рецепты", callback_data="my_recipes"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_settings_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="✏️ Изменить предпочтения", callback_data="edit_preferences")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_recipe_main_kb(recipe_id: int) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="👀 Показать шаги приготовления", callback_data=f"show_steps_{recipe_id}")],
        [InlineKeyboardButton(text="🛒 Показать ингредиенты", callback_data=f"ingredients_{recipe_id}")],
        [InlineKeyboardButton(text="➡️ Следующий рецепт", callback_data="next_recipe")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_step_navigation_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="➡️ Следующий шаг", callback_data="next_step")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_back_to_recipe_kb(recipe_id: int) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="🔙 Вернуться к рецепту", callback_data=f"back_to_recipe_{recipe_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_buy_subscription_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="💳 Оформить подписку", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_subscription_kb(buttons: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def get_meal_type_kb() -> InlineKeyboardMarkup:
    meal_types = await sync_to_async(list)(MealTime.objects.all())
    inline_keyboard = [
        [InlineKeyboardButton(text=meal.name, callback_data=f"meal_{meal.id}")]
        for meal in meal_types
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def get_categories_kb() -> InlineKeyboardMarkup:
    categories = await sync_to_async(list)(Category.objects.all())
    buttons = [
        [InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")]
        for category in categories
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_meal_types")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_restart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Начать заново", callback_data="restart_preferences")]
    ])

def get_restart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_main_menu")]
    ])
