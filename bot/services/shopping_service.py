from asgiref.sync import sync_to_async

from bot.logic.shopping_service import ShoppingService as LogicShoppingService
from bot.exceptions import BotError

class ShoppingService:
    """
    Адаптер для Telegram-бота: асинхронно вызывает логику сборки списка покупок.
    """

    @staticmethod
    @sync_to_async
    def get_list(telegram_id: int):
        try:
            lines = LogicShoppingService(
                planner_engine=None,   
                prefs_repo=None      
            ).build_list(
                telegram_id=telegram_id,
                start=None, 
                days=7
            )
            return lines
        except Exception as e:
            raise BotError(f"Ошибка при формировании списка покупок: {e}")
