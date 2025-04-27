# bot/services/planner_service.py

import os
import django
from datetime import date
from asgiref.sync import sync_to_async

from bot.logic.planner_service import PlannerService as LogicPlannerService
from bot.logic.exceptions import BotError
from bot.logic.simple_planner_engine import SimplePlannerEngine
from bot.adapters.user_repository import DjangoUserPreferencesRepository
from bot.adapters.recipe_repository import DjangoRecipeRepository
from bot.adapters.feedback_repository import DjangoFeedbackRepository

# Инициализируем Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodplan.settings")
django.setup()

class PlannerService:
    """
    Асинхронный адаптер для Telegram-бота:
    обёртка синхронного PlannerService из bot.logic.
    """

    def __init__(self):
        engine = SimplePlannerEngine(
            recipe_repo=DjangoRecipeRepository(),
            feedback_repo=DjangoFeedbackRepository(),
            prefs_repo=DjangoUserPreferencesRepository()
        )
        self._service = LogicPlannerService(
            engine=engine,
            prefs_repo=DjangoUserPreferencesRepository()
        )

    @sync_to_async
    def plan_week(self, telegram_id: int, start_date: date = None):
        """
        Асинхронно вызывает планировщик:
        - start_date: дата начала (по умолчанию сегодня)
        """
        try:
            start = start_date or date.today()
            return self._service.plan_week(
                telegram_id=telegram_id,
                start=start
            )
        except Exception as e:
            raise BotError(f"Не удалось составить план меню: {e}")
