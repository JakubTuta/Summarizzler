from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="user_id",
    )
    favorites = models.ManyToManyField(
        "Summary.Summary",
        related_name="users",
        blank=True,
    )

    def __str__(self):
        return self.user.username
