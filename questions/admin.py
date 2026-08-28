
from django.contrib import admin
from .models import Subject, Question, Choice, WrittenQuestion
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name","code","display_order")
    search_fields = ("name","code")
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_number","subject","exam_session","normalized_answer","is_resolved","has_explanation","difficulty")
    list_filter = ("is_resolved","has_explanation","difficulty","subject")
    search_fields = ("question_text","source_answer")
    list_select_related = ("exam_session","subject")
    readonly_fields = ("source_hash","original_source_text","created_at")
    actions = ["mark_active","mark_inactive"]
    def mark_active(self, request, queryset):
        queryset.update(active=True)
    def mark_inactive(self, request, queryset):
        queryset.update(active=False)
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question","label","is_correct")
    list_filter = ("is_correct","label")
@admin.register(WrittenQuestion)
class WrittenQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_number","subject","exam_session","marks")
    search_fields = ("question_text",)
