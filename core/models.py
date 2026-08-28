from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    class Type(models.TextChoices):
        ACHIEVEMENT = "ACHIEVEMENT", "Achievement"
        LEVEL_UP = "LEVEL_UP", "Level Up"
        STREAK = "STREAK", "Streak"
        DAILY = "DAILY", "Daily Challenge"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.title}"
