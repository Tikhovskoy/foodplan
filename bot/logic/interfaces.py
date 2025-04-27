from typing import Protocol, List
from datetime import date
from decimal import Decimal
from bot.logic.dto import UserPreferences

class Recipe:
    """Интерфейс рецепта для логики бота и тестов."""
    id: int
    title: str
    description: str
    ingredients: List['Ingredient']
    is_vegan: bool
    is_gluten_free: bool
    estimated_cost: Decimal

class Ingredient:
    """Интерфейс ингредиента для логики бота и тестов."""
    name: str
    amount: float
    unit: str

class PlannedMeal:
    """Запланированное блюдо на дату."""
    recipe: Recipe
    date: date

class IRecipeRepository(Protocol):
    def list_active(self) -> List[Recipe]:
        """Возвращает все активные рецепты."""

class IFeedbackRepository(Protocol):
    def list_disliked(self, telegram_id: int) -> List[int]:
        """Список ID рецептов, которые пользователь дизлайкнул."""
    
    def save_feedback(self, telegram_id: int, recipe_id: int, kind: str) -> None:
        """Сохраняет лайк/дизлайк."""

class ISubscriptionRepository(Protocol):
    def is_active(self, telegram_id: int) -> bool:
        """Проверяет, есть ли у пользователя активная подписка."""
    
    def extend(self, telegram_id: int, days: int) -> None:
        """Продлевает подписку на days дней."""

class IUserPreferencesRepository(Protocol):
    def get(self, telegram_id: int) -> UserPreferences:
        """Получить настройки пользователя."""
    
    def save(self, telegram_id: int, prefs: UserPreferences) -> None:
        """Сохранить настройки пользователя."""

class IPlannerEngine(Protocol):
    def plan_menu(
        self,
        telegram_id: int,
        start: date,
        days: int,
        prefs: UserPreferences
    ) -> List[PlannedMeal]:
        """Строит план меню на заданное число дней."""

class ISubscriptionService(Protocol):
    async def check_active(self, telegram_id: int) -> bool:
        """Проверяет активность подписки."""
