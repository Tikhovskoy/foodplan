from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Category
from recipes.models import Recipe, Ingredient
from payments.models import SubscriptionPlan

User = get_user_model()


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pass"
        )
        self.client.force_login(self.admin)

    def test_admin_index(self):
        """Админка доступна и отдаёт 200 на главную страницу."""
        url = reverse("admin:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_category_changelist(self):
        """Страница списка категорий отдаёт 200."""
        url = reverse("admin:users_category_changelist")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_recipe_changelist(self):
        """Страница списка рецептов отдаёт 200."""
        url = reverse("admin:recipes_recipe_changelist")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_subscriptionplan_changelist(self):
        """Страница списка тарифных планов отдаёт 200."""
        url = reverse("admin:payments_subscriptionplan_changelist")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_add_category_via_admin(self):
        """Можно создать новую категорию через админку."""
        url = reverse("admin:users_category_add")
        resp = self.client.post(url, {"name": "TestCat"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Category.objects.filter(name="TestCat").exists())

    def test_add_recipe_with_ingredient_via_admin(self):
        """
        Проверяем, что на форме добавления рецепта
        можно одновременно добавить один ингредиент.
        """
        cat = Category.objects.create(name="TestCat")
        ing = Ingredient.objects.create(name="Ing1")

        url = reverse("admin:recipes_recipe_add")
        data = {
            "title": "MyRecipe",
            "categories": [cat.pk],
            "estimated_cost": "0.00",
            "recipeingredient_set-TOTAL_FORMS": "1",
            "recipeingredient_set-INITIAL_FORMS": "0",
            "recipeingredient_set-MIN_NUM_FORMS": "0",
            "recipeingredient_set-MAX_NUM_FORMS": "1000",
            "recipeingredient_set-0-ingredient": str(ing.pk),
            "recipeingredient_set-0-amount": "2.00",
            "recipeingredient_set-0-unit": "pcs",
            "recipeingredient_set-0-unit_cost": "15.50",
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Recipe.objects.filter(title="MyRecipe").exists())
        recipe = Recipe.objects.get(title="MyRecipe")
        self.assertEqual(str(recipe.estimated_cost), "31.00")
