from rest_framework import serializers
from Users.models import UserData

from . import models


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Summary
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "category",
            "content_type",
            "user_prompt",
            "likes",
            "dislikes",
            "favorites",
            "tags",
            "created_at",
            "is_private",
            "url",
            "raw_text",
        )

    def create(self, validated_data):
        summary = models.Summary.objects.create(**validated_data)
        return summary


class SummaryPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Summary
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "category",
            "content_type",
            # "user_prompt",
            "likes",
            # "dislikes",
            "favorites",
            # "tags",
            "created_at",
            "is_private",
            # "url",
            # "raw_text",
        )
