from datetime import date
from typing import List
from bot.logic.interfaces import IPlannerEngine, IUserPreferencesRepository, PlannedMeal
from bot.logic.exceptions import PlannerError

class PlannerService:
    def __init__(
        self,
        engine: IPlannerEngine,
        prefs_repo: IUserPreferencesRepository
    ):
        self._engine = engine
        self._prefs = prefs_repo

    def plan_week(self, telegram_id: int, start: date) -> List[PlannedMeal]:
        """
        Составляет меню на 7 дней, начиная с start.
        Бросает PlannerError при любых ошибках.
        """
        prefs = self._prefs.get(telegram_id)
        try:
            return self._engine.plan_menu(
                telegram_id=telegram_id,
                start=start,
                days=7,
                prefs=prefs
            )
        except Exception as e:
            raise PlannerError(f"Не удалось составить план: {e}")
