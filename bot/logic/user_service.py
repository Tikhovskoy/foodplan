import random
from typing import List, Optional

from bot.logic.interfaces import IUserPreferencesRepository
from bot.logic.dto import UserPreferences
from bot.logic.exceptions import PreferenceError, RecipeAlreadyLiked, RecipeAlreadyDisliked
from recipes.models import Recipe
from users.models import Profile
from django.utils.timezone import now



class UserService:
    def __init__(self, prefs_repo: IUserPreferencesRepository):
        self.prefs_repo = prefs_repo

    def get_preferences(self, telegram_id: int) -> UserPreferences:
        return self.prefs_repo.get(telegram_id=telegram_id)

    def toggle(self, telegram_id: int, category: str) -> UserPreferences:
        prefs = self.prefs_repo.get(telegram_id)
        if category in prefs.categories:
            prefs.categories.remove(category)
        else:
            prefs.categories.append(category)
        self.prefs_repo.save(telegram_id, prefs)
        return prefs

    def set_categories(self, telegram_id: int, new_categories: List[str]) -> UserPreferences:
        if not all(isinstance(c, str) for c in new_categories):
            raise PreferenceError("Категории должны быть строками")
        prefs = UserPreferences(categories=new_categories)
        self.prefs_repo.save(telegram_id, prefs)
        return prefs

    def like_recipe(self, telegram_id: int, recipe_id: int) -> UserPreferences:
        profile = self._get_profile(telegram_id)
        recipe = Recipe.objects.get(id=recipe_id)

        if profile.liked.filter(id=recipe_id).exists():
            raise RecipeAlreadyLiked("Рецепт уже в списке понравившихся")

        profile.disliked.remove(recipe)
        profile.liked.add(recipe)

        prefs = self.prefs_repo.get(telegram_id)
        if recipe_id not in prefs.liked_recipes:
            prefs.liked_recipes.append(recipe_id)
        if recipe_id in prefs.disliked_recipes:
            prefs.disliked_recipes.remove(recipe_id)
        self.prefs_repo.save(telegram_id, prefs)

        return prefs

    def dislike_recipe(self, telegram_id: int, recipe_id: int) -> UserPreferences:
        profile = self._get_profile(telegram_id)
        recipe = Recipe.objects.get(id=recipe_id)

        if profile.disliked.filter(id=recipe_id).exists():
            raise RecipeAlreadyDisliked("Рецепт уже в списке непонравившихся")

        profile.liked.remove(recipe)
        profile.disliked.add(recipe)

        prefs = self.prefs_repo.get(telegram_id)
        if recipe_id not in prefs.disliked_recipes:
            prefs.disliked_recipes.append(recipe_id)
        if recipe_id in prefs.liked_recipes:
            prefs.liked_recipes.remove(recipe_id)
        self.prefs_repo.save(telegram_id, prefs)

        return prefs

    def list_liked_recipes(self, telegram_id: int) -> List[Recipe]:
        return list(self._get_profile(telegram_id).liked.all())

    def list_disliked_recipes(self, telegram_id: int) -> List[Recipe]:
        return list(self._get_profile(telegram_id).disliked.all())

    def recommend_recipe(self, telegram_id: int) -> Optional[Recipe]:
        prefs = self.prefs_repo.get(telegram_id)

        if not prefs.categories:
            return None

        recipes = Recipe.objects.filter(
            categories__name__in=prefs.categories
        ).exclude(
            id__in=prefs.disliked_recipes
        ).distinct()

        return random.choice(list(recipes)) if recipes else None

    def _get_profile(self, telegram_id: int) -> Profile:
        return Profile.objects.select_related("user").get(user__telegram_id=telegram_id)
    
    def skip_recipe(self, telegram_id: int, current_recipe_id: int) -> Optional[Recipe]:
        prefs = self.prefs_repo.get(telegram_id)

        recipes = Recipe.objects.filter(
            categories__name__in=prefs.categories
        ).exclude(
            id__in=prefs.disliked_recipes + [current_recipe_id]
        ).distinct()

        return random.choice(list(recipes)) if recipes.exists() else None
    
    def can_receive_recipe(self, telegram_id: int) -> bool:
        profile = self._get_profile(telegram_id)
        return profile.is_active_subscriber() or profile.can_get_free_recipe()

    def get_daily_recipe(self, telegram_id: int) -> Optional[Recipe]:
        profile = self._get_profile(telegram_id)
        prefs = self.prefs_repo.get(telegram_id)

        if not prefs.categories:
            return None

        recipes = Recipe.objects.filter(
            categories__name__in=prefs.categories
        ).exclude(
            id__in=prefs.disliked_recipes
        ).distinct()

        if not recipes.exists():
            return None

        if profile.is_active_subscriber():
            return random.choice(list(recipes))

        today = now().date()
        if profile.last_free_recipe == today:
            return None

        profile.last_free_recipe = today
        profile.save()
        return random.choice(list(recipes))

    def can_view_ingredients(self, telegram_id: int) -> bool:
        profile = self._get_profile(telegram_id)
        return profile.is_active_subscriber()

    def has_category(self, telegram_id: int, category: str) -> bool:
        prefs = self.prefs_repo.get(telegram_id=telegram_id)
        return category in prefs.categories


