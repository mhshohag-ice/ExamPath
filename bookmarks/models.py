from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="bookmarked_by")
    note = models.TextField(blank=True, help_text="Personal note")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ("user", "question")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} bookmarked Q{self.question.question_number}"


class QuestionNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_notes")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "question")

    def __str__(self):
        return f"Note by {self.user.username} on Q{self.question_id}"
