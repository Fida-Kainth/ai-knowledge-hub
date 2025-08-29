from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()

class ArticlesAPITest(APITestCase):
    def setUp(self):
        # create two users
        self.user1 = User.objects.create_user(username="alice", email="alice@example.com", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", email="bob@example.com", password="pass1234")
        # create articles
        self.art1 = Article.objects.create(author=self.user1, title="AI Intro", content="Content about AI", tags=["ai","intro"])
        self.art2 = Article.objects.create(author=self.user2, title="Django Tips", content="Django content", tags=["django","tutorial"])

    def test_list_articles(self):
        url = reverse("articles-list-create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)

    def test_search_q(self):
        url = reverse("articles-list-create") + "?q=django"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "Django Tips")

    def test_search_tag(self):
        url = reverse("articles-list-create") + "?tag=ai"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [a["title"] for a in resp.data]
        self.assertIn("AI Intro", titles)

    def test_create_article_requires_auth(self):
        url = reverse("articles-list-create")
        payload = {"title": "New", "content": "New content", "tags": ["x"]}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate and retry
        self.client.force_authenticate(user=self.user1)
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], "New")
        self.client.force_authenticate(user=None)

    def test_retrieve_update_delete(self):
        url = reverse("articles-detail", args=[self.art1.id])
        # retrieve
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # update - must authenticate
        self.client.force_authenticate(user=self.user1)
        resp = self.client.put(url, {"title": "AI Intro Updated", "content": "Updated", "tags": ["ai"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "AI Intro Updated")
        # delete by non-author should fail
        self.client.force_authenticate(user=self.user2)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # delete by author
        self.client.force_authenticate(user=self.user1)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
