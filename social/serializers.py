from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "image",
            "created_on",
            "author",
            "shared_user",
            "shared_body,",
            "shared_on",
            "likes",
            "dislikes",
            "tags",
        )
