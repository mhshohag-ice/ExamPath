
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Bookmark, QuestionNote
from questions.models import Question
from quiz.models import UserAnswer

@login_required
def bookmark_list(request):
    tab = request.GET.get("tab","bookmarked")
    # Bookmarked
    if tab == "bookmarked":
        qs = Question.objects.filter(bookmarked_by__user=request.user).select_related("exam_session","subject")
    elif tab == "incorrect":
        incorrect_ids = UserAnswer.objects.filter(attempt__user=request.user, is_correct=False).values_list("question_id", flat=True)
        qs = Question.objects.filter(id__in=incorrect_ids).select_related("exam_session","subject").distinct()
    elif tab == "difficult":
        # difficult = high incorrect count globally? or user incorrect?
        qs = Question.objects.filter(user_answers__attempt__user=request.user, user_answers__is_correct=False).annotate(inc=Q(user_answers__is_correct=False)).distinct()
        # fallback to bookmarked if not enough
        if not qs.exists():
            qs = Question.objects.filter(bookmarked_by__user=request.user)
    elif tab == "recent":
        recent_ids = UserAnswer.objects.filter(attempt__user=request.user).order_by("-answered_at").values_list("question_id", flat=True)[:50]
        qs = Question.objects.filter(id__in=recent_ids).select_related("exam_session","subject")
    else:
        qs = Question.objects.filter(bookmarked_by__user=request.user)
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "bookmarks/list.html", {"questions": page, "tab": tab})

@login_required
def my_questions(request):
    return bookmark_list(request)
