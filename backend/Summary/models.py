from django.db import models


class Summary(models.Model):
    url = models.TextField()
    title = models.TextField()
    content_type = models.CharField(max_length=10)
    summary = models.TextField()
    author = models.ForeignKey(
        "Users.UserData",
        on_delete=models.CASCADE,
        related_name="summaries",
    )
    user_prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
