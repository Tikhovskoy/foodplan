from django.utils import timezone
from .models import Profile
from recipes.models import Recipe

class UserRepository:
    """
    Репозиторий для работы с профилем пользователя.
    """
    def get_profile(self, user_id: int) -> Profile:
        return Profile.objects.get(user__id=user_id)

    def update_preferences(
        self, user_id: int,
        vegan: bool, gluten_free: bool, budget_mode: bool
    ) -> Profile:
        profile = self.get_profile(user_id)
        profile.vegan = vegan
        profile.gluten_free = gluten_free
        profile.budget_mode = budget_mode
        profile.save(update_fields=['vegan', 'gluten_free', 'budget_mode'])
        return profile

    def like_recipe(self, user_id: int, recipe: Recipe) -> Profile:
        profile = self.get_profile(user_id)
        profile.liked.add(recipe)
        return profile

    def dislike_recipe(self, user_id: int, recipe: Recipe) -> Profile:
        profile = self.get_profile(user_id)
        profile.disliked.add(recipe)
        return profile

    def increment_swap_count(self, user_id: int) -> Profile:
        profile = self.get_profile(user_id)
        profile.swap_count += 1
        profile.save(update_fields=['swap_count'])
        return profile

    def mark_free_recipe(self, user_id: int) -> Profile:
        profile = self.get_profile(user_id)
        profile.mark_free_recipe_given()
        return profile

    def extend_subscription(self, user_id: int, days: int) -> Profile:
        profile = self.get_profile(user_id)
        today = timezone.now().date()
        profile.paid_until = today + timezone.timedelta(days=days)
        profile.save(update_fields=['paid_until'])
        return profile
