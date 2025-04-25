from typing import Protocol, List, Optional
from datetime import date


class IRecipeRepository(Protocol):
    def list_active(self) -> List["Recipe"]:
        """Возвращает все активные рецепты."""


class IFeedbackRepository(Protocol):
    def list_disliked(self, telegram_id: int) -> List[int]:
        """Список ID рецептов, которые пользователь дизлайкнул."""

    def save_feedback(self, telegram_id: int, recipe_id: int, kind: str) -> None:
        """Сохраняет лайк/дизлайк."""


class IUserPreferencesRepository(Protocol):
    def get(self, telegram_id: int) -> "UserPreferences":
        """Настройки пользователя."""

    def save(self, telegram_id: int, prefs: "UserPreferences") -> None:
        """Сохраняет настройки пользователя."""


class ISubscriptionRepository(Protocol):
    def is_active(self, telegram_id: int) -> bool:
        """Есть ли у пользователя активная подписка?"""

    def extend(self, telegram_id: int, days: int) -> None:
        """Продлить подписку на N дней."""


class IPlannerEngine(Protocol):
    def plan_menu(
        self,
        telegram_id: int,
        start: date,
        days: int,
        prefs: "UserPreferences"
    ) -> List["PlannedMeal"]:
        """Составляет меню на период."""



class Recipe:
    id: int
    title: str
    description: str
    estimated_cost: float
    ingredients: List["Ingredient"]


class Ingredient:
    name: str
    amount: float
    unit: str


class UserPreferences:
    def __init__(self, categories: Optional[List[str]] = None):
        self.categories = categories or []


class PlannedMeal:
    recipe: Recipe
    date: date
