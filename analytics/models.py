from django.db import models

# Analytics is largely derived from QuizAttempt/UserAnswer but we can have materialized helpers
# For now, keep empty but provide helper functions

class UserSubjectPerformance(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="subject_performances")
    subject = models.ForeignKey("questions.Subject", on_delete=models.CASCADE)
    attempted = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    avg_time_seconds = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "subject")
        indexes = [
            models.Index(fields=["user", "accuracy"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}: {self.accuracy}%"
