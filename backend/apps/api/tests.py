from django.urls import reverse_lazy
from rest_framework import status
#  internals
from apps.tests.base import BaseTestCase


class ApiViewsTestCase(BaseTestCase):
    def test_hi_view(self):
        res = self.client.get(reverse_lazy("api:hi"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), {"message": "Hello world!"})

    def test_hi_view_TR_language(self):
        res = self.client.get(reverse_lazy("api:hi"), headers={
                              "Accept-Language": "tr"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), {"message": "Merhaba dünya!"})

    def test_CustomTokenObtainPairView(self):
        payload = {
            "username": self.user.username,
            "password": self.user_password
        }
        res = self.client.post(reverse_lazy("api:token-obtain"), data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertTrue("refresh" in res_json)
        self.assertTrue("access" in res_json)
        self.assertTrue(len(res_json["refresh"]) > 0)
        self.assertTrue(len(res_json["access"]) > 0)
