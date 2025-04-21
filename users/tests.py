from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 't@test.com', 'pass')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_auto_created(self):
        self.assertIsInstance(self.profile, Profile)

    def test_is_active_subscriber(self):
        self.profile.paid_until = timezone.now().date() + timedelta(days=1)
        self.assertTrue(self.profile.is_active_subscriber())
        self.profile.paid_until = timezone.now().date() - timedelta(days=1)
        self.assertFalse(self.profile.is_active_subscriber())

    def test_free_recipe_flag(self):
        self.profile.last_free_recipe = None
        self.assertTrue(self.profile.can_get_free_recipe())
        self.profile.last_free_recipe = timezone.now().date()
        self.assertFalse(self.profile.can_get_free_recipe())

    def test_mark_free_recipe(self):
        self.profile.mark_free_recipe_given()
        self.assertEqual(self.profile.last_free_recipe, timezone.now().date())
