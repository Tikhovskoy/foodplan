from collections import defaultdict
from datetime import date
from typing import List
from bot.logic.interfaces import IPlannerEngine, IUserPreferencesRepository
from bot.logic.exceptions import ShoppingError

class ShoppingService:
    def __init__(
        self,
        planner_engine: IPlannerEngine,
        prefs_repo: IUserPreferencesRepository
    ):
        self._engine = planner_engine
        self._prefs = prefs_repo

    def build_list(
        self,
        telegram_id: int,
        start: date,
        days: int = 7
    ) -> List[str]:
        """
        Генерирует список покупок по меню:
         - агрегирует одинаковые ингредиенты
         - возвращает список строк вида "2.00 кг картофеля"
        """
        prefs = self._prefs.get(telegram_id)
        try:
            meals = self._engine.plan_menu(
                telegram_id=telegram_id,
                start=start,
                days=days,
                prefs=prefs
            )
        except Exception as e:
            raise ShoppingError(f"Не удалось получить меню: {e}")

        agg: dict[tuple[str, str], float] = defaultdict(float)
        for meal in meals:
            for ing in meal.recipe.ingredients:
                key = (ing.name, ing.unit)
                agg[key] += ing.amount

        return [f"{amount:.2f} {unit} {name}" for (name, unit), amount in agg.items()]
