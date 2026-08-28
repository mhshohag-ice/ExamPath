from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quiz(models.Model):
    class QuizMode(models.TextChoices):
        PRACTICE = "PRACTICE", "Practice"
        EXAM = "EXAM", "Exam Simulation"
        QUICK = "QUICK", "Quick Quiz"
        SUBJECT = "SUBJECT", "Subject Practice"
        WEAK = "WEAK", "Weak Area"
        INCORRECT = "INCORRECT", "Incorrect Review"
        BOOKMARKED = "BOOKMARKED", "Bookmarked"
        RANDOM = "RANDOM", "Random Challenge"
        DAILY = "DAILY", "Daily Challenge"

    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=220, blank=True)
    mode = models.CharField(max_length=20, choices=QuizMode.choices, default=QuizMode.PRACTICE, db_index=True)
    exam_session = models.ForeignKey("exams.ExamSession", null=True, blank=True, on_delete=models.SET_NULL, related_name="quizzes")
    subject = models.ForeignKey("questions.Subject", null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=False)
    time_limit_minutes = models.IntegerField(null=True, blank=True, help_text="For exam mode")
    question_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_mode_display()} - {self.title or self.id}"


class QuizAttempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        ABANDONED = "ABANDONED", "Abandoned"
        TIMED_OUT = "TIMED_OUT", "Timed Out"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, null=True, blank=True, on_delete=models.SET_NULL, related_name="attempts")
    exam_session = models.ForeignKey("exams.ExamSession", null=True, blank=True, on_delete=models.CASCADE, related_name="attempts")
    mode = models.CharField(max_length=20, choices=Quiz.QuizMode.choices, default=Quiz.QuizMode.PRACTICE)
    subject = models.ForeignKey("questions.Subject", null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS, db_index=True)
    score = models.FloatField(default=0)  # percentage
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    # For exam integrity
    current_question_index = models.IntegerField(default=0)
    time_remaining_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "exam_session"]),
            models.Index(fields=["user", "-started_at"]),
        ]

    def __str__(self):
        return f"Attempt {self.id} by {self.user.username} - {self.score}%"

    def calculate_score(self):
        total = self.total_questions or self.answers.count()
        if total == 0:
            self.score = 0
        else:
            self.score = round((self.correct_count / total) * 100, 2)
        return self.score

    def duration_display(self):
        secs = self.time_taken_seconds
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        if h:
            return f"{h}h {m}m {s}s"
        if m:
            return f"{m}m {s}s"
        return f"{s}s"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="user_answers")
    selected_choice = models.ForeignKey("questions.Choice", null=True, blank=True, on_delete=models.SET_NULL)
    selected_label = models.CharField(max_length=1, blank=True, choices=[("A","A"),("B","B"),("C","C"),("D","D")])
    is_correct = models.BooleanField(default=False, db_index=True)
    time_taken_seconds = models.IntegerField(default=0)
    marked_for_review = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    is_skipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ("attempt", "question")
        indexes = [
            models.Index(fields=["attempt", "is_correct"]),
            models.Index(fields=["question", "is_correct"]),
        ]

    def __str__(self):
        return f"{self.attempt.id} - Q{self.question.question_number} - {self.selected_label or 'skip'} {'✓' if self.is_correct else '✗'}"

    def save(self, *args, **kwargs):
        # auto-determine is_correct if not set
        if self.selected_label and self.question_id:
            correct = self.question.normalized_answer
            if correct:
                self.is_correct = (self.selected_label.upper() == correct.upper())
            else:
                self.is_correct = False
        elif not self.selected_label:
            self.is_skipped = True
            self.is_correct = False
        super().save(*args, **kwargs)


class QuestionReview(models.Model):
    """Spaced repetition / review tracking per user per question"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_reviews")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="reviews")
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    correct_streak = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    next_review_at = models.DateTimeField(null=True, blank=True, db_index=True)
    confidence = models.FloatField(default=0)  # 0-1
    easiness = models.FloatField(default=2.5)  # SM-2 like

    class Meta:
        unique_together = ("user", "question")
        indexes = [
            models.Index(fields=["user", "next_review_at"]),
        ]

    def __str__(self):
        return f"Review {self.user.username} Q{self.question_id} streak={self.correct_streak}"
