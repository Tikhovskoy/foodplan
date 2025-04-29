from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_meal_type_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🍳 Завтрак", callback_data="meal_breakfast"),
            InlineKeyboardButton(text="🍽️ Обед", callback_data="meal_lunch"),
        ],
        [
            InlineKeyboardButton(text="🍝 Ужин", callback_data="meal_dinner"),
            InlineKeyboardButton(text="🍏 Перекус", callback_data="meal_snack"),
        ],
    ])
    return kb
