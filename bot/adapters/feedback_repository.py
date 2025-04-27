from typing import List
from users.models import Profile
from recipes.models import Recipe
from asgiref.sync import sync_to_async

class DjangoFeedbackRepository:

    @sync_to_async
    def list_disliked(self, telegram_id: int) -> List[int]:
        try:
            profile = Profile.objects.get(user__telegram_id=telegram_id)
            return list(profile.disliked.values_list("id", flat=True))
        except Profile.DoesNotExist:
            return []

    def save_feedback(self, telegram_id: int, recipe_id: int, kind: str) -> None:
        profile = Profile.objects.get(user__telegram_id=telegram_id)
        recipe = Recipe.objects.get(id=recipe_id)
        if kind == "like":
            profile.liked.add(recipe)
        elif kind == "dislike":
            profile.disliked.add(recipe)
