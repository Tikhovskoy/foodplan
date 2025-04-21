from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile, Category
from .models import Recipe
from .services import RecipeRepository
import random

class RecipeRepositoryCategoryTest(TestCase):
    def setUp(self):
        self.repo = RecipeRepository()
        self.user = User.objects.create_user("u1", "u1@example.com", "pass")
        self.profile = Profile.objects.get(user=self.user)

        # категории
        self.c1 = Category.objects.create(name="Веган")
        self.c2 = Category.objects.create(name="Без глютена")

        # рецепты
        self.r1 = Recipe.objects.create(title="Vegan Salad", estimated_cost=0)
        self.r1.categories.add(self.c1)
        self.r2 = Recipe.objects.create(title="GF Soup", estimated_cost=0)
        self.r2.categories.add(self.c2)
        self.r3 = Recipe.objects.create(title="All Inclusive", estimated_cost=0)
        self.r3.categories.add(self.c1, self.c2)

        random.choice = lambda seq: seq[0]

    def test_no_categories(self):
        got = self.repo.get_random(self.profile)
        self.assertIn(got, [self.r1, self.r2, self.r3])

    def test_single_category(self):
        self.profile.categories.add(self.c1)
        got = self.repo.get_random(self.profile)
        self.assertEqual(got, self.r1)

    def test_multiple_categories(self):
        self.profile.categories.add(self.c1, self.c2)
        got = self.repo.get_random(self.profile)
        self.assertEqual(got, self.r1)

    def test_exclude_disliked(self):
        self.profile.categories.add(self.c1)
        self.profile.disliked.add(self.r1)
        got = self.repo.get_random(self.profile)
        self.assertEqual(got, self.r3)

    def test_no_match(self):
        other = Category.objects.create(name="Эконом")
        self.profile.categories.add(other)
        got = self.repo.get_random(self.profile)
        self.assertIsNone(got)
