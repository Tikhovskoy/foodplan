from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="subscribe_yes")],
            [InlineKeyboardButton(text="❌ Нет", callback_data="subscribe_no")]
        ]
    )

def get_buy_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Купить подписку", callback_data="buy_subscription")],
            [InlineKeyboardButton(text="❌ Отказаться", callback_data="decline_subscription")]
        ]
    )

def get_meal_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍳 Завтрак", callback_data="meal_breakfast")],
            [InlineKeyboardButton(text="🍝 Обед", callback_data="meal_lunch")],
            [InlineKeyboardButton(text="🍽 Ужин", callback_data="meal_dinner")]
        ]
    )

def get_diet_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🥦 Веган", callback_data="diet_vegan")],
            [InlineKeyboardButton(text="🌾 Без глютена", callback_data="diet_glutenfree")],
            [InlineKeyboardButton(text="🍖 Без ограничений", callback_data="diet_none")]
        ]
    )

def get_recipe_main_kb(recipe_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Показать шаги", callback_data=f"show_steps_{recipe_id}")],
            [InlineKeyboardButton(text="🛒 Ингредиенты", callback_data=f"ingredients_{recipe_id}")],
            [
                InlineKeyboardButton(text="👍 Лайк", callback_data=f"like_{recipe_id}"),
                InlineKeyboardButton(text="👎 Дизлайк", callback_data=f"dislike_{recipe_id}")
            ],
            [InlineKeyboardButton(text="➡️ Следующий рецепт", callback_data="next_recipe")]
        ]
    )

def get_step_navigation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующий шаг", callback_data="next_step")]
        ]
    )

def get_start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Начать", callback_data="start")]
        ]
    )

def get_back_to_recipe_kb(recipe_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться к рецепту", callback_data=f"back_to_recipe_{recipe_id}")]
        ]
    )