from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Level(models.Model):
    number = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=100)
    xp_threshold = models.IntegerField(help_text="Cumulative XP required to reach this level")
    badge_icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon or emoji")
    color = models.CharField(max_length=20, default="#0d6efd")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Level {self.number}: {self.title} ({self.xp_threshold} XP)"


class XPTransaction(models.Model):
    class Source(models.TextChoices):
        CORRECT_ANSWER = "CORRECT_ANSWER", "Correct Answer"
        QUIZ_COMPLETED = "QUIZ_COMPLETED", "Quiz Completed"
        DAILY_CHALLENGE = "DAILY_CHALLENGE", "Daily Challenge"
        PERFECT_QUIZ = "PERFECT_QUIZ", "Perfect Quiz"
        EXAM_COMPLETED = "EXAM_COMPLETED", "Exam Completed"
        REVIEW_WRONG = "REVIEW_WRONG", "Review Wrong Answers"
        STREAK_BONUS = "STREAK_BONUS", "Streak Bonus"
        ACHIEVEMENT = "ACHIEVEMENT", "Achievement"
        MANUAL = "MANUAL", "Manual"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="xp_transactions")
    amount = models.IntegerField()
    source = models.CharField(max_length=30, choices=Source.choices, db_index=True)
    reference_type = models.CharField(max_length=100, blank=True)
    reference_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "source"]),
        ]

    def __str__(self):
        return f"{self.user.username} +{self.amount} XP ({self.source})"


class Achievement(models.Model):
    code = models.SlugField(unique=True, help_text="e.g., first_answer, century")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="🏆")
    xp_reward = models.IntegerField(default=0)
    # Rule definition (JSON): e.g., {"type":"questions_answered","threshold":100}
    rule_type = models.CharField(max_length=50, db_index=True, help_text="Rule engine type")
    rule_threshold = models.IntegerField(default=1)
    rule_config = models.JSONField(default=dict, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="unlocks")
    unlocked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    xp_awarded = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"


class LeaderboardSnapshot(models.Model):
    PERIOD_CHOICES = [
        ("weekly","Weekly"),
        ("monthly","Monthly"),
        ("all","All Time"),
    ]
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaderboard_snapshots")
    xp = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    snapshot_date = models.DateField(default=timezone.now, db_index=True)

    class Meta:
        unique_together = ("period","user","snapshot_date")
        ordering = ["period","rank"]


# Helper functions for gamification logic
XP_RULES = {
    "CORRECT_ANSWER": 10,
    "QUIZ_COMPLETED": 25,
    "DAILY_CHALLENGE": 50,
    "PERFECT_QUIZ": 50,
    "EXAM_COMPLETED": 100,
    "REVIEW_WRONG": 20,
}

def calculate_level_for_xp(xp):
    """Return level number for given XP based on Level thresholds"""
    from django.db.models import Max
    # Levels are thresholds inclusive
    lvl = Level.objects.filter(xp_threshold__lte=xp).order_by("-number").first()
    return lvl.number if lvl else 1

def award_xp(user, amount, source, reference_type="", reference_id=None, description=""):
    from accounts.models import Profile
    tx = XPTransaction.objects.create(
        user=user, amount=amount, source=source,
        reference_type=reference_type, reference_id=reference_id, description=description
    )
    # Update profile xp_total atomically
    profile, _ = Profile.objects.get_or_create(user=user)
    from django.db.models import F
    Profile.objects.filter(user=user).update(xp_total=F('xp_total') + amount)
    profile.refresh_from_db()
    # Check level up
    new_level = calculate_level_for_xp(profile.xp_total)
    if new_level != profile.level:
        profile.level = new_level
        profile.save(update_fields=["level"])
    return tx
