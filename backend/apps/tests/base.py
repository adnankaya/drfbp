from django.test import TestCase
from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
#  globals
User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User(username="tester", email="tester@example.com",
                         first_name="tester first", last_name="tester last",
                         phone="5559998877")
        self.user_password = "qwert"
        self.user.set_password(self.user_password)
        self.user.save()

    @property
    def auth_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {"HTTP_AUTHORIZATION": f'Token {refresh.access_token}'}

    def tearDown(self) -> None:
        return super().tearDown()
