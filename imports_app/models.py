from django.db import models
from django.contrib.auth.models import User


class QuestionImport(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        PREVIEW = "PREVIEW", "Preview"
        APPROVED = "APPROVED", "Approved"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    filename = models.CharField(max_length=500)
    file_path = models.CharField(max_length=1000, blank=True)
    file_hash = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    total_records = models.IntegerField(default=0)
    imported = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    duplicates = models.IntegerField(default=0)
    invalid = models.IntegerField(default=0)
    warnings_count = models.IntegerField(default=0)
    errors_count = models.IntegerField(default=0)
    processing_time_seconds = models.FloatField(default=0)
    report = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Import {self.filename} - {self.status}"


class QuestionImportError(models.Model):
    import_job = models.ForeignKey(QuestionImport, on_delete=models.CASCADE, related_name="errors")
    row_number = models.IntegerField(null=True, blank=True)
    question_number = models.IntegerField(null=True, blank=True)
    exam_route_id = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    raw_data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Error: {self.message[:100]}"


class QuestionImportWarning(models.Model):
    import_job = models.ForeignKey(QuestionImport, on_delete=models.CASCADE, related_name="warnings")
    row_number = models.IntegerField(null=True, blank=True)
    question_number = models.IntegerField(null=True, blank=True)
    exam_route_id = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    raw_data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Warning: {self.message[:100]}"


class QuestionImportDuplicate(models.Model):
    import_job = models.ForeignKey(QuestionImport, on_delete=models.CASCADE, related_name="duplicates_entries")
    question_text = models.TextField()
    source_hash = models.CharField(max_length=64, db_index=True)
    existing_question_id = models.IntegerField(null=True, blank=True)
    similarity = models.FloatField(default=1.0)
    raw_data = models.TextField(blank=True)
    decision = models.CharField(max_length=20, default="PENDING", choices=[("PENDING","Pending"),("KEEP","Keep Both"),("MERGE","Merge"),("IGNORE","Ignore")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Duplicate {self.source_hash[:8]} sim={self.similarity}"
