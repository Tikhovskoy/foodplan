from django.core.management.base import BaseCommand
import asyncio
from bot.main import main  # путь к твоей функции main()

class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **options):
        asyncio.run(main())