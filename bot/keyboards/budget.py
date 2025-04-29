from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_budget_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Эконом", callback_data="budget_economy"),
            InlineKeyboardButton(text="Стандарт", callback_data="budget_standard"),
        ],
        [
            InlineKeyboardButton(text="Премиум", callback_data="budget_premium"),
        ],
    ])
    return kb
