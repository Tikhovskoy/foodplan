import random
from .models import Recipe

class RecipeRepository:
    def get_by_id(self, recipe_id: int) -> Recipe:
        return Recipe.objects.get(pk=recipe_id)

    def list_all(self):
        return Recipe.objects.all()

    def get_random(self, profile=None) -> Recipe:
        qs = Recipe.objects.all().order_by('pk')
        if profile:
            cats = profile.categories.values_list('id', flat=True)
            if cats:
                qs = qs.filter(categories__id__in=cats)
            disliked = profile.disliked.values_list('id', flat=True)
            if disliked:
                qs = qs.exclude(id__in=disliked)
            qs = qs.distinct().order_by('pk')
        lst = list(qs)
        return random.choice(lst) if lst else None
