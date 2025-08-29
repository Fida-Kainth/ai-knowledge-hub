from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "content", "author", "tags", "source", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def get_author(self, obj):
        # Represent author as dict to avoid importing user serializer
        user = obj.author
        return {"id": user.id, "username": getattr(user, "username", None), "email": getattr(user, "email", None)}

    def validate_tags(self, value):
        # Ensure tags is a list of strings
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("tags must be a list of strings")
        for t in value:
            if not isinstance(t, str):
                raise serializers.ValidationError("each tag must be a string")
        return value
