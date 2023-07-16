from django.contrib.auth import get_user_model
from model_bakery import baker
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
#  internals
from apps.tests.base import BaseTestCase

#  globals
User = get_user_model()


class UsersViewsTests(BaseTestCase):
    """python manage.py test apps.users.tests.test_views.UsersViewsTests"""

    def test_ListUsersAPIView(self):
        #  create 2 users
        baker.make(User, username="user1")
        baker.make(User, username="user2")
        res = self.client.get(
            reverse_lazy("api:users:list-users"), **self.auth_token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), User.objects.count())
        usernames = [r.get("username") for r in res_json]
        self.assertTrue(User.objects.filter(username__in=usernames).exists())

    def test_CreateUserAPIView(self):
        payload = {
            "username": "adnan",
            "email": "adnankaya@example.com",
            "password": "qwert",
            "password2": "qwert",
            "first_name": "adnan",
            "last_name": "kaya",
            "phone": "5554443322",

        }
        res = self.client.post(
            reverse_lazy("api:users:create-user"), data=payload,
            **self.auth_token)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_json = res.json()
        self.assertEqual(payload["username"], res_json["username"])
        self.assertEqual(payload["email"], res_json["email"])
        self.assertEqual(payload["first_name"], res_json["first_name"])
        self.assertEqual(payload["last_name"], res_json["last_name"])
        self.assertEqual(payload["phone"], res_json["phone"])
        self.assertTrue("id" in res_json)
        self.assertFalse(res_json["email_verified"])

    def test_UserViewset_detail(self):
        res = self.client.get(
            reverse_lazy("api:users:detail-user", args=[self.user.id]),
            **self.auth_token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertTrue("id" in res_json)
        self.assertEqual(res_json["id"], self.user.id)
        self.assertEqual(res_json["username"], self.user.username)
        self.assertEqual(res_json["email"], self.user.email)
        self.assertEqual(res_json["phone"], self.user.phone)
        self.assertEqual(res_json["first_name"], self.user.first_name)
        self.assertEqual(res_json["last_name"], self.user.last_name)
        self.assertEqual(res_json["email_verified"], False)

    def test_UserViewset_put(self):
        update_obj = baker.make(User, username="u_user",
                                email="u_email@example.com")
        payload = {
            "username": "new_user",
            "email": "new_user_email@example.com",
            "phone": "5550005555",
            "first_name": "new first",
            "last_name": "new last",
        }
        res = self.client.put(
            reverse_lazy("api:users:detail-user", args=[update_obj.id]),
            data=payload,
            **self.auth_token,
            content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertTrue("id" in res_json)
        self.assertEqual(payload["username"], res_json["username"])
        self.assertEqual(payload["email"], res_json["email"])
        self.assertEqual(payload["first_name"], res_json["first_name"])
        self.assertEqual(payload["last_name"], res_json["last_name"])
        self.assertEqual(payload["phone"], res_json["phone"])

    def test_UserViewset_patch(self):
        update_obj = baker.make(User, username="u_user",
                                email="u_email@example.com")
        payload = {
            "email": "new_user_email@example.com",
        }
        res = self.client.patch(
            reverse_lazy("api:users:detail-user", args=[update_obj.id]),
            data=payload,
            **self.auth_token,
            content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertTrue("id" in res_json)
        self.assertEqual(payload["email"], res_json["email"])

    def test_DeactivateUserView(self):
        u_user = baker.make(User, username="u_user",
                                email="u_email@example.com")
        self.user = u_user
        res = self.client.delete(
            reverse_lazy("api:users:deactivate-user", args=[u_user.id]),
            **self.auth_token)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_UserViewset_password_change(self):
        u_user1 = baker.make(User, username="u_user1",
                             email="u_email1@example.com")
        u_user1.set_password("qwert")
        u_user1.save()
        u_user2 = baker.make(User, username="u_user2",
                             email="u_email2@example.com")
        u_user2.set_password("qwert")
        u_user2.save()

        # set base user as u_user1
        self.user = u_user1
        payload = {
            "old_password": "qwert",
            "password": "asdfg",
            "password2": "asdfg",
        }
        res = self.client.patch(
            reverse_lazy("api:users:password-change", args=(u_user2.id,)),
            data=payload,
            **self.auth_token,
            content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res_json = res.json()
        self.assertEqual(
            res_json[0], 'Requested user is not the owner of this user object')
        # set base user as u_user2
        self.user = u_user2
        res = self.client.patch(
            reverse_lazy("api:users:password-change", args=(u_user2.id,)),
            data=payload,
            **self.auth_token,
            content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(res_json, {'message': 'password changed'})
