from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class UserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="user_id",
    )
    likes = models.ManyToManyField(
        "Summary.Summary",
        related_name="liked_by",
        blank=True,
    )
    dislikes = models.ManyToManyField(
        "Summary.Summary",
        related_name="disliked_by",
        blank=True,
    )
    favorites = models.ManyToManyField(
        "Summary.Summary",
        related_name="favored_by",
        blank=True,
    )

    def __str__(self):
        return self.user.username
