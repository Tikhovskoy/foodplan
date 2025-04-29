import os
import django
import random
import requests
from decimal import Decimal
from datetime import date, timedelta
from django.core.files.base import ContentFile

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodplan.settings")
django.setup()

# Модели
from users.models import TelegramUser, Profile, Category
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeStep
from payments.models import SubscriptionPlan, Subscription

# Ссылки на изображения (Unsplash, желательно подбирать тематические)
image_urls = [
    "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
    "https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642",
    "https://images.unsplash.com/photo-1613145993484-ccd7a3c3b48f",
    "https://images.unsplash.com/photo-1612197553264-bdfd7d14f9aa",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
    "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
    "https://images.unsplash.com/photo-1562967916-eb82221dfb36",
    "https://images.unsplash.com/photo-1490645935967-10de6ba17061",
    "https://images.unsplash.com/photo-1512058564366-c9e3e0464e57",
]

# Загрузка и прикрепление изображения к рецепту
def download_image(url, recipe):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_name = f"{recipe.title.replace(' ', '_')}.jpg"
        recipe.image.save(file_name, ContentFile(response.content), save=True)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

def run():
    print("Заполнение тестовыми данными...")

    # Категории
    category_names = ["Веган", "Без глютена", "Эконом", "Кето", "Праздничное"]
    categories = [Category.objects.get_or_create(name=name)[0] for name in category_names]

    # Пользователь и профиль
    user, _ = User.objects.get_or_create(username="testuser", telegram_id=123456)
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.categories.set(random.sample(categories, 2))
    profile.paid_until = date.today() + timedelta(days=30)
    profile.save()

    # Ингредиенты
    ingredient_names = ["Картофель", "Морковь", "Лук", "Масло", "Соль", "Кабачок", "Чеснок", "Томаты", "Горошек", "Петрушка"]
    ingredients = [Ingredient.objects.get_or_create(name=name)[0] for name in ingredient_names]

    # Рецепты (10 штук)
    for i in range(10):
        title = f"Овощное рагу #{i + 1}"
        recipe = Recipe.objects.create(title=title, estimated_cost=Decimal("0.00"))
        recipe.categories.set(random.sample(categories, k=2))

        selected_ingredients = random.sample(ingredients, k=4)
        for ing in selected_ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ing,
                amount=random.randint(1, 5),
                unit="pcs",
                unit_cost=Decimal("10.00")
            )

        # Шаги приготовления
        RecipeStep.objects.create(recipe=recipe, order=1, text="Очистить овощи")
        RecipeStep.objects.create(recipe=recipe, order=2, text="Нарезать и обжарить")

        # Стоимость
        recipe.recalc_cost()

        # Фото
        download_image(random.choice(image_urls), recipe)

    # Тариф и подписка
    plan, _ = SubscriptionPlan.objects.get_or_create(
        name="Месячная",
        price=Decimal("199.00"),
        duration=30,
        defaults={"description": "Подписка на месяц"}
    )
    Subscription.objects.get_or_create(user=user, plan=plan)

    print("Готово! Проверь в админке 😉")

if __name__ == "__main__":
    run()
