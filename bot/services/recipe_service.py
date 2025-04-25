from asgiref.sync import sync_to_async
from recipes.models import Recipe, RecipeFeedback
from bot.exceptions import RecipeNotFound

class RecipeService:
    @staticmethod
    @sync_to_async
    def fetch_random(telegram_id: int, vegan=False, gluten_free=False, budget=None):
        qs = Recipe.objects.filter(is_active=True)
        if vegan:        qs = qs.filter(is_vegan=True)
        if gluten_free:  qs = qs.filter(is_gluten_free=True)
        if budget is not None:
            qs = qs.filter(estimated_cost__lte=budget)
        disliked = RecipeFeedback.objects.filter(
            user__telegram_id=telegram_id, kind='dislike'
        ).values_list('recipe_id', flat=True)
        qs = qs.exclude(id__in=list(disliked))
        r = qs.order_by("?").first()
        if not r:
            raise RecipeNotFound("Нет рецептов по вашим фильтрам")
        return r

    @staticmethod
    @sync_to_async
    def save_feedback(telegram_id: int, recipe_id: int, kind: str):
        RecipeFeedback.objects.create(
            user_id=telegram_id, recipe_id=recipe_id, kind=kind
        )
