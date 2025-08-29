from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Article
from .serializers import ArticleSerializer

class ArticleListCreateView(generics.ListCreateAPIView):
    """
    GET: list articles with optional ?q=search & ?tag=tagname
    POST: create article (authenticated)
    """
    queryset = Article.objects.all().select_related("author")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        tag = self.request.query_params.get("tag")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(source__icontains=q))
        if tag:
            # tags is a JSON list field; use contains for simple match
            qs = qs.filter(tags__contains=[tag])
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET / PUT / PATCH / DELETE a single article.
    Only authenticated users can modify; deletion allowed for author or staff.
    """
    queryset = Article.objects.all().select_related("author")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # keep author as-is; update timestamp handled by model
        serializer.save()

    def delete(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        if article.author != user and not user.is_staff:
            return Response({"detail": "You do not have permission to delete this article."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

