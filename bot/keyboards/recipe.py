from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_recipe_kb(recipe_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️ Нравится", callback_data=f"like_{recipe_id}"),
            InlineKeyboardButton(text="👎 Не нравится", callback_data=f"dislike_{recipe_id}"),
        ],
        [
            InlineKeyboardButton(text="🍴 Показать ингредиенты", callback_data=f"ingredients_{recipe_id}"),
            InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_recipe"),
        ],
    ])
    return kb
