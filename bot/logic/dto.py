from dataclasses import dataclass, field
from typing import List

@dataclass
class UserPreferences:
    categories: List[str] = field(default_factory=list)
    liked_recipes: List[int] = field(default_factory=list)
    disliked_recipes: List[int] = field(default_factory=list)
