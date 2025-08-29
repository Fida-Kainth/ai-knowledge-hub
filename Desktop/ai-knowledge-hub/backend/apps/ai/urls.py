from django.urls import path
from .views import QueryAIView, EmbeddingsView

urlpatterns = [
    path("query", QueryAIView.as_view(), name="ai_query"),
    path("embeddings", EmbeddingsView.as_view(), name="ai_embeddings"),
]
