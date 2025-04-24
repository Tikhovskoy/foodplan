import asyncio
import logging
import os
import django

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config.config import settings
from .handlers import register_all_handlers
import sys
from pathlib import Path

# Добавим корень проекта в PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
# Настройки логгирования
logging.basicConfig(level=logging.INFO)

# Подключение Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodplan.settings")
django.setup()  # Важно: поднимает Django ORM и конфигурации

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    register_all_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
