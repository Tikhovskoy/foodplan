from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal

@dataclass
class UserPreferences:
    """
    Настройки пользователя для подбора рецептов и планирования:
    - categories: выбранные текстовые категории
    - vegan: учитывать веганские блюда
    - gluten_free: учитывать безглютенные блюда
    - budget: максимальная стоимость рецепта
    - liked_recipes: список ID лайкнутых рецептов
    - disliked_recipes: список ID дизлайкнутых рецептов
    """
    categories: List[str] = field(default_factory=list)
    vegan: bool = False
    gluten_free: bool = False
    budget: Optional[Decimal] = None
    liked_recipes: List[int] = field(default_factory=list)
    disliked_recipes: List[int] = field(default_factory=list)
