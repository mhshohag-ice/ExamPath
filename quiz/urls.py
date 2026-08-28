
from django.urls import path
from . import views
urlpatterns = [
    path("start/", views.start_quiz, name="quiz_start"),
    path("start/<slug:slug>/", views.start_quiz, name="quiz_start_exam"),
    path("exam/<slug:slug>/", views.exam_mode_start, name="quiz_exam_start"),
    path("<int:attempt_id>/", views.quiz_take, name="quiz_take"),
    path("<int:attempt_id>/answer/", views.quiz_answer, name="quiz_answer"),
    path("<int:attempt_id>/submit/", views.quiz_submit, name="quiz_submit"),
    path("<int:attempt_id>/result/", views.quiz_result, name="quiz_result"),
    path("history/", views.quiz_history, name="quiz_history"),
]
