from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "username",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class UserDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = models.UserData
        fields = (
            "username",
            "email",
            "favorites",
        )

    def create(self, validated_data):
        user = self.context["user"]
        user_data = models.UserData.objects.create(user=user, **validated_data)

        return user_data


class UserDataDeserializer:
    def __init__(self, model: models.UserData):
        self.model = model

    def deserialize(self):
        return {
            "username": self.model.user.username,
            "email": self.model.user.email,
            "favorites": self.model.favorites.values_list("id", flat=True),
        }
