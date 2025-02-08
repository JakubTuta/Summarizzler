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
            "user_prompt",  # Add this line to include user_prompt as well
            "created_at",
            "likes",
            "dislikes",
            "favorites",
        )

    def create(self, validated_data):
        summary = models.Summary.objects.create(**validated_data)
        return summary
