
from django.contrib import admin
from .models import QuestionImport, QuestionImportError, QuestionImportWarning, QuestionImportDuplicate
@admin.register(QuestionImport)
class QuestionImportAdmin(admin.ModelAdmin):
    list_display = ("filename","status","total_records","imported","skipped","duplicates","invalid","warnings_count","created_at")
    list_filter = ("status",)
    readonly_fields = ("report","file_hash")
@admin.register(QuestionImportError)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("import_job","exam_route_id","question_number","message")
@admin.register(QuestionImportWarning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ("import_job","exam_route_id","question_number","message")
@admin.register(QuestionImportDuplicate)
class DuplicateAdmin(admin.ModelAdmin):
    list_display = ("import_job","source_hash","similarity","decision")
