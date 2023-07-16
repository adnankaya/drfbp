from decimal import Decimal
import datetime
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model


User = get_user_model()



# @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class BaseTestCase(TestCase):

    def create_user(self):
        User = get_user_model()
        self.user_tester = User.objects.create_user(email='user.tester@example.com',
                                        username='tester',
                                        phone='5554445555',
                                        password='password')
    
    def setUp(self):
        res = super(BaseTestCase, self).setUp()

        self.create_user()

        return res
