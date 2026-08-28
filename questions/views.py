
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Question, Subject, Choice
from exams.models import ExamSession
from bookmarks.models import Bookmark
from quiz.models import UserAnswer

def question_list(request):
    qs = Question.objects.select_related("exam_session","subject").filter(active=True)
    q = request.GET.get("q","")
    subject = request.GET.get("subject","")
    exam = request.GET.get("exam","")
    has_explanation = request.GET.get("has_explanation","")
    resolved = request.GET.get("resolved","")
    if q:
        qs = qs.filter(Q(question_text__icontains=q) | Q(explanation__icontains=q))
    if subject:
        qs = qs.filter(subject__slug=subject)
    if exam:
        # Support both slug and route_id (case-insensitive) for exact serial filtering
        qs = qs.filter(Q(exam_session__slug=exam) | Q(exam_session__slug__iexact=exam) | Q(exam_session__route_id=exam) | Q(exam_session__route_id__iexact=exam))
    if has_explanation == "1":
        qs = qs.filter(has_explanation=True)
    if resolved == "1":
        qs = qs.filter(is_resolved=True)
    elif resolved == "0":
        qs = qs.filter(is_resolved=False)
    # Maintain exact serial as per uttoron.academy source: exam insertion order (route) + question_number
    # When filtered by single exam, ordering by question_number guarantees Q1..QN exact.
    # For global list, group by exam_session then serial.
    if exam:
        qs = qs.order_by("question_number")
    else:
        qs = qs.order_by("exam_session", "question_number")
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    subjects = Subject.objects.all()
    exams = ExamSession.objects.all()[:20]
    # bookmarks for user
    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(Bookmark.objects.filter(user=request.user).values_list("question_id", flat=True))
    return render(request, "questions/list.html", {"questions": page, "q": q, "subjects": subjects, "exams": exams, "bookmarked_ids": bookmarked_ids})

def question_detail(request, pk):
    question = get_object_or_404(Question.objects.select_related("exam_session","subject"), pk=pk)
    choices = question.choices.all()
    is_bookmarked = False
    user_answer = None
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, question=question).exists()
        # last attempt answer?
        user_answer = UserAnswer.objects.filter(attempt__user=request.user, question=question).order_by("-answered_at").first()
    return render(request, "questions/detail.html", {"question": question, "choices": choices, "is_bookmarked": is_bookmarked, "user_answer": user_answer})

@login_required
@require_POST
def bookmark_toggle(request, pk):
    question = get_object_or_404(Question, pk=pk)
    bm, created = Bookmark.objects.get_or_create(user=request.user, question=question)
    if not created:
        bm.delete()
        return JsonResponse({"bookmarked": False})
    return JsonResponse({"bookmarked": True})

def written_list(request):
    from .models import WrittenQuestion
    # Maintain exact serial for written: exam_session then question_number
    qs = WrittenQuestion.objects.select_related("exam_session","subject").all().order_by("exam_session", "question_number")
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "questions/written_list.html", {"questions": page})
