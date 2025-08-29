from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AiApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="aiuser", email="ai@example.com", password="password123")
        # authenticate using DRF test client helper
        self.client.force_authenticate(user=self.user)

    def test_query_ai_requires_prompt(self):
        url = reverse("ai_query")
        resp = self.client.post(url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_ai_returns_answer(self):
        url = reverse("ai_query")
        resp = self.client.post(url, {"prompt": "Hello world"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("answer", resp.data)
        self.assertIsInstance(resp.data["answer"], str)

    def test_embeddings_endpoint(self):
        url = reverse("ai_embeddings")
        resp = self.client.post(url, {"texts": ["hello", "world"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("embeddings", resp.data)
        self.assertEqual(len(resp.data["embeddings"]), 2)
