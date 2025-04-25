from asgiref.sync import sync_to_async
from planner.services import calculate_shopping_list
from bot.exceptions import BotError

class ShoppingService:
    @staticmethod
    @sync_to_async
    def get_list(telegram_id: int):
        try:
            return calculate_shopping_list(telegram_id)
        except Exception:
            raise BotError("Ошибка при формировании списка покупок")
