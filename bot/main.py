# file: bot/main.py

import os
import asyncio
import logging
import django

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv

# ───── Инициализация Django ─────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodplan.settings")
django.setup()

# ───── Загрузка переменных окружения ─────
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ───── Настройка логгера ─────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ───── Импорт хендлеров ─────
from bot.handlers.start import router as start_router
from bot.handlers.recipe import router as recipe_router
from bot.handlers.subscribe import router as subscribe_router
# TODO: shopping_router, settings_router...

# ───── Создание и запуск ─────
async def main():
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(recipe_router)
    dp.include_router(subscribe_router)

    logger.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
