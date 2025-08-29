from django.db import models
from django.conf import settings

class Article(models.Model):
    """
    Article model for CRUD and simple search.
    - tags stored as JSON list (Django 3.1+ JSONField).
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    title = models.CharField(max_length=512)
    content = models.TextField()
    tags = models.JSONField(default=list, blank=True)  # e.g. ["ai","tutorial"]
    source = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.author})"
