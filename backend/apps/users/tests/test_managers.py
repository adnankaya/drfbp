from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com',
                                        username='normal',
                                        phone='5554443322',
                                        password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'normal')
        self.assertEqual(user.phone, '5554443322')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.username)
            self.assertIsNotNone(user.phone)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(email='u@user.com',
                                     phone='5554443322', password="foo")
        with self.assertRaises(TypeError):
            User.objects.create_user(email='u@user.com',
                                     username='u', password="foo")
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='u',
                                     phone='5554443322', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com',
                                                   username='super',
                                                   phone='5554443322',
                                                   password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super')
        self.assertEqual(admin_user.phone, '5554443322')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.username)
            self.assertIsNotNone(admin_user.phone)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@user.com',
                                          username='super', phone='5554443322',
                                          password='foo', is_superuser=False)
