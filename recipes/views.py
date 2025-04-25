from django.views.generic.detail import DetailView
from .models import Recipe

class RecipeDetail(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"
