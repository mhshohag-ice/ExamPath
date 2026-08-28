
from django.contrib import admin
from .models import Quiz, QuizAttempt, UserAnswer, QuestionReview
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id","user","mode","exam_session","score","status","started_at")
    list_filter = ("mode","status")
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt","question","selected_label","is_correct")
@admin.register(QuestionReview)
class QuestionReviewAdmin(admin.ModelAdmin):
    list_display = ("user","question","correct_streak","next_review_at")
