from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_register(self):
        url = reverse("user-register")
        data = {"username": "newuser", "email": "new@example.com", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse("user-login")
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_profile(self):
        url = reverse("user-profile")
        token = self.client.post(reverse("user-login"), {"email": "test@example.com", "password": "password123"}).data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

