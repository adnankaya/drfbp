from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError
from model_bakery import baker
#  internals


User = get_user_model()


class UsersModelsTests(TestCase):
    def setUp(self) -> None:
        res = super().setUp()
        return res


