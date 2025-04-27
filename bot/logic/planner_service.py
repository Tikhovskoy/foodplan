# bot/logic/planner_service.py

from datetime import date
from typing import List

from bot.logic.interfaces import IPlannerEngine, IUserPreferencesRepository, PlannedMeal
from bot.logic.exceptions import PlannerError

class PlannerService:
    """
    Сервис бизнес-логики: обёртка над движком планирования меню.
    """

    def __init__(self, engine: IPlannerEngine, prefs_repo: IUserPreferencesRepository):
        # Должны быть именно эти имена engine и prefs_repo
        self._engine = engine
        self._prefs_repo = prefs_repo

    def plan_week(self, telegram_id: int, start: date) -> List[PlannedMeal]:
        """
        Составляет меню на 7 дней, начиная с даты `start`.
        Бросает PlannerError при ошибке.
        """
        prefs = self._prefs_repo.get(telegram_id)
        try:
            return self._engine.plan_menu(
                telegram_id=telegram_id,
                start=start,
                days=7,
                prefs=prefs
            )
        except Exception as e:
            raise PlannerError(f"Не удалось составить план меню: {e}")
