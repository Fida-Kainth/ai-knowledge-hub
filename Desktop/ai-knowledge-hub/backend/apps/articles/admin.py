from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "source", "created_at", "updated_at")
    search_fields = ("title", "content", "source")
    list_filter = ("created_at", "updated_at")
