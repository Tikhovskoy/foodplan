from django.urls import path
from .views import RecipeDetail

app_name = "recipes"

urlpatterns = [
    path("<int:pk>/", RecipeDetail.as_view(), name="recipe-detail"),
]
