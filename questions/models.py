import hashlib
from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Uppercase code like MENTAL-ABILITY")
    display_order = models.IntegerField(default=0, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name.upper().replace(" ", "-")
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"
        UNKNOWN = "UNKNOWN", "Unknown"

    exam_session = models.ForeignKey("exams.ExamSession", on_delete=models.CASCADE, related_name="questions")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="questions")
    question_number = models.IntegerField(db_index=True)
    question_text = models.TextField(help_text="Original question text, preserves Bengali + LaTeX")
    explanation = models.TextField(blank=True, help_text="Original explanation")
    source_answer = models.CharField(max_length=10, blank=True, help_text="Original answer: a,b,c,d,Blank")
    normalized_answer = models.CharField(max_length=1, blank=True, null=True, choices=[("A","A"),("B","B"),("C","C"),("D","D")], db_index=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.UNKNOWN, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    has_explanation = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=True, help_text="False if Blank/missing answer")
    source_hash = models.CharField(max_length=64, db_index=True, help_text="SHA256 of normalized question text for dedup")
    original_source_text = models.TextField(blank=True, help_text="Keeps raw markdown snippet for audit")
    # Audit
    modified_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["exam_session", "question_number"]
        unique_together = ("exam_session", "question_number")
        indexes = [
            models.Index(fields=["exam_session", "subject"]),
            models.Index(fields=["source_hash"]),
            models.Index(fields=["normalized_answer"]),
            models.Index(fields=["is_resolved"]),
        ]

    def __str__(self):
        return f"Q{self.question_number} [{self.subject}] {self.question_text[:60]}"

    def save(self, *args, **kwargs):
        if not self.source_hash:
            # normalize: lower, strip, collapse whitespace
            import re
            norm = re.sub(r'\s+', ' ', self.question_text.strip().lower())
            self.source_hash = hashlib.sha256(norm.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    @property
    def has_blank_answer(self):
        return not self.normalized_answer

    @property
    def is_bookmarked_by(self):
        # helper for template
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    label = models.CharField(max_length=1, choices=[("A","A"),("B","B"),("C","C"),("D","D")])
    text = models.TextField(help_text="Option text, Bengali/LaTeX preserved")
    is_correct = models.BooleanField(default=False, db_index=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["display_order"]
        unique_together = ("question", "label")
        indexes = [
            models.Index(fields=["question", "label"]),
        ]

    def __str__(self):
        return f"{self.label}. {self.text[:50]} {'(correct)' if self.is_correct else ''}"


class WrittenQuestion(models.Model):
    exam_session = models.ForeignKey("exams.ExamSession", on_delete=models.CASCADE, related_name="written_questions")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="written_questions")
    question_number = models.IntegerField(db_index=True)
    # Written fields
    question_text = models.TextField()
    marks = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=50, blank=True)
    set_name = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=100, blank=True)
    instructions = models.TextField(blank=True)
    model_answer = models.TextField(blank=True, help_text="If available")
    explanation = models.TextField(blank=True)
    source_hash = models.CharField(max_length=64, db_index=True)
    original_source_text = models.TextField(blank=True)
    exam_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["exam_session", "question_number"]
        unique_together = ("exam_session", "question_number")

    def __str__(self):
        return f"Written Q{self.question_number} [{self.subject}]"

    def save(self, *args, **kwargs):
        import hashlib, re
        if not self.source_hash:
            norm = re.sub(r'\s+', ' ', self.question_text.strip().lower())
            self.source_hash = hashlib.sha256(norm.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
