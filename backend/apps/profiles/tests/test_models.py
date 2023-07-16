from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker


User = get_user_model()


class ProfileModelsTests(TestCase):
    """
    python manage.py test apps.profiles.tests.test_models.ProfileModelsTests
    """

    def test_create_profile(self):
        user = User.objects.create_user(email='user@example.com',
                                        username='user',
                                        phone='5554443322',
                                        password='password')
        profile = baker.make("profiles.Profile", user=user,
                             )

        self.assertEqual(user.username, profile.user.username)

    def test_create_profile_settings(self):
        user = User.objects.create_user(email='user@example.com',
                                        username='user',
                                        phone='5554443322',
                                        password='password')
        profile = baker.make("profiles.Profile", user=user,
                             )
        profile_settings = baker.make("profiles.ProfileSettings", profile=profile,
                                      name="settings1", enabled=True)

        self.assertTrue(profile_settings.enabled)
