from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    # Gamification snapshot
    xp_total = models.IntegerField(default=0, db_index=True)
    level = models.IntegerField(default=1, db_index=True)
    # Streaks
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    streak_freeze_count = models.IntegerField(default=0)
    # Preferences
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default="en", choices=[("en","English"),("bn","Bengali")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def update_streak(self, activity_date=None):
        if activity_date is None:
            activity_date = timezone.localdate()
        if self.last_activity_date is None:
            self.current_streak = 1
            self.longest_streak = max(self.longest_streak, 1)
            self.last_activity_date = activity_date
            self.save(update_fields=["current_streak","longest_streak","last_activity_date","updated_at"])
            return
        delta = (activity_date - self.last_activity_date).days
        if delta == 0:
            return
        elif delta == 1:
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
        elif delta > 1:
            self.current_streak = 1
        self.last_activity_date = activity_date
        self.save(update_fields=["current_streak","longest_streak","last_activity_date","updated_at"])


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_activities")
    date = models.DateField(db_index=True)
    questions_answered = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    streak_maintained = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user","date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.questions_answered} Qs"
