from rest_framework import serializers
from Users.models import UserData

from . import models


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Summary
        fields = (
            "id",
            "url",
            "title",
            "content_type",
            "summary",
            "author",
            "user_prompt",
            "is_private",
            "likes",
            "dislikes",
            "favorites",
            "created_at",
        )

    def create(self, validated_data):
        summary = models.Summary.objects.create(**validated_data)
        return summary
