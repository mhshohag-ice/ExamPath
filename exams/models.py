from django.db import models
from django.utils.text import slugify


class ExamFamily(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=110, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon or emoji")
    active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Exam Families"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ExamSession(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CANCELLED = "CANCELLED", "Cancelled"
        ARCHIVED = "ARCHIVED", "Archived"
        DEMO = "DEMO", "Demo"

    exam_family = models.ForeignKey(ExamFamily, on_delete=models.CASCADE, related_name="sessions")
    name = models.CharField(max_length=200, db_index=True)  # e.g., "50th BCS"
    slug = models.SlugField(max_length=220, unique=True)
    route_id = models.CharField(max_length=100, unique=True, db_index=True, help_text="Original route-id, case-sensitive")
    exam_type = models.CharField(max_length=100, default="General", help_text="General, Special (Health) etc.")
    specialization = models.CharField(max_length=120, blank=True, help_text="e.g., Medical, Dental, Education")
    exam_date = models.DateField(null=True, blank=True, db_index=True)
    marks = models.IntegerField(default=100)
    question_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    source_preview_url = models.URLField(blank=True, max_length=500)
    source_exam_url = models.URLField(blank=True, max_length=500)
    description = models.TextField(blank=True)
    is_demo = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-exam_date", "-created_at"]
        indexes = [
            models.Index(fields=["exam_family", "status"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["route_id"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.exam_type}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.name} {self.exam_type} {self.route_id}"
            self.slug = slugify(base)[:210]
            # ensure uniqueness
            orig = self.slug
            counter = 1
            while ExamSession.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        # For special exams, show full distinction
        if self.specialization:
            return f"{self.name} - {self.specialization}"
        if self.exam_type and self.exam_type.lower() != "general":
            return f"{self.name} - {self.exam_type}"
        return self.name
