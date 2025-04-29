from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_diet_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Обычная", callback_data="diet_regular"),
            InlineKeyboardButton(text="Вегетарианская", callback_data="diet_vegetarian"),
        ],
        [
            InlineKeyboardButton(text="Кето", callback_data="diet_keto"),
            InlineKeyboardButton(text="Палео", callback_data="diet_paleo"),
        ],
    ])
    return kb
