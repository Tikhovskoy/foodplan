from asgiref.sync import sync_to_async
from users.models import Profile, Category
from recipes.models import Recipe
from bot.logic.dto import UserPreferences
from bot.exceptions import PreferenceError

class DjangoUserPreferencesRepository:
    @sync_to_async
    def get(self, telegram_id: int) -> UserPreferences:
        profile = Profile.objects.select_related("user").get(user__telegram_id=telegram_id)

        category_names = list(profile.categories.values_list("name", flat=True))
        liked_ids = list(profile.liked.values_list("id", flat=True))
        disliked_ids = list(profile.disliked.values_list("id", flat=True))

        return UserPreferences(
            categories=category_names,
            liked_recipes=liked_ids,
            disliked_recipes=disliked_ids,
        )

    @sync_to_async
    def save(self, telegram_id: int, prefs: UserPreferences) -> None:
        profile = Profile.objects.select_related("user").get(user__telegram_id=telegram_id)

        profile.categories.clear()

        for name in prefs.categories:
            try:
                category = Category.objects.get(name__iexact=name)
                profile.categories.add(category)
            except Category.DoesNotExist:
                raise PreferenceError(f"Категория '{name}' не найдена")

        profile.liked.set(Recipe.objects.filter(id__in=prefs.liked_recipes))
        profile.disliked.set(Recipe.objects.filter(id__in=prefs.disliked_recipes))

        profile.save()
