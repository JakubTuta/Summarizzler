import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


def generate_uuid():
    return uuid.uuid4().int % (2**63)


class Summary(models.Model):
    # pk
    id = models.BigIntegerField(primary_key=True, default=generate_uuid, editable=False)
    # required
    title = models.TextField(default="")
    summary = models.TextField(default="")
    author = models.ForeignKey(
        "Users.UserData",
        on_delete=models.CASCADE,
        related_name="summaries",
    )
    category = models.CharField(
        max_length=20, default=""
    )  # technology, business, health & wellness, education, lifestyle, entertainment, science, politics, art & culture, sports, food & drink, travel, other,
    content_type = models.CharField(
        max_length=10, default=""
    )  # text, website, file, video
    user_prompt = models.TextField(default="")

    # not required
    likes = models.ManyToManyField(
        "Users.UserData", related_name="liked_summaries", blank=True
    )
    dislikes = models.ManyToManyField(
        "Users.UserData", related_name="disliked_summaries", blank=True
    )
    favorites = models.ManyToManyField(
        "Users.UserData", related_name="favorite_summaries", blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=30, blank=True), default=list, blank=True
    )
    is_private = models.BooleanField(default=False, blank=True)

    # website
    url = models.TextField(blank=True, default="")

    # text / file
    raw_text = models.TextField(blank=True, default="")

    # Auto-generated
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
