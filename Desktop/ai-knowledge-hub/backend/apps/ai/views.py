from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings

from .llm_service import query_llm
from .embeddings import embed_texts

class QueryAIView(APIView):
    """
    POST /api/ai/query
    Body: {"prompt": "...", "options": {...}}
    Returns: {"answer": "..."}
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt", "")
        options = request.data.get("options", {}) or {}

        if not prompt:
            return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Simple synchronous call to query LLM
        try:
            answer = query_llm(prompt, options)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"answer": answer})

class EmbeddingsView(APIView):
    """
    POST /api/ai/embeddings
    Body: {"texts": ["a","b",...]}
    Returns: {"embeddings": [[...], [...]]}
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        texts = request.data.get("texts") or []
        if not isinstance(texts, list) or not texts:
            return Response({"detail": "texts must be a non-empty list"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vectors = embed_texts(texts)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"embeddings": vectors})
