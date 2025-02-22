import re

import Users.functions as users_functions
import Users.serializers as users_serializers
from rest_framework import serializers

from . import models


class SummarySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

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
        author = self.context.get("author", None)
        if author:
            validated_data["author"] = author

        summary = models.Summary.objects.create(**validated_data)
        return summary

    def get_author(self, obj):
        author = users_functions.find_user_data(user=obj.author)

        if author:
            return users_serializers.UserDataSerializer(author).data

        return None


class SummaryPreviewSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Summary
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "category",
            "content_type",
            "likes",
            "favorites",
            "created_at",
            "is_private",
        )

    def get_summary(self, obj):
        if not obj.summary:
            return ""

        return re.sub(r"<[^>]*>", "", obj.summary[:100])

    def get_author(self, obj):
        author = users_functions.find_user_data(user=obj.author)

        if author:
            return users_serializers.UserDataSerializer(author).data

        return None
