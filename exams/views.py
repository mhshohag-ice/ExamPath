
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from .models import ExamSession, ExamFamily
from questions.models import Question, Subject
from quiz.models import QuizAttempt

def exam_list(request):
    q = request.GET.get("q","").strip()
    subject_slug = request.GET.get("subject","")
    status_filter = request.GET.get("status","")
    sort = request.GET.get("sort","-exam_date")
    exams = ExamSession.objects.select_related("exam_family").annotate(question_count_actual=Count("questions"))
    if q:
        exams = exams.filter(Q(name__icontains=q) | Q(route_id__icontains=q) | Q(exam_type__icontains=q))
    if subject_slug:
        exams = exams.filter(questions__subject__slug=subject_slug).distinct()
    if status_filter:
        exams = exams.filter(status=status_filter)
    # sort options
    allowed = {"-exam_date":"-exam_date","exam_date":"exam_date","-question_count":"-question_count","name":"name"}
    exams = exams.order_by(allowed.get(sort,"-exam_date"))
    paginator = Paginator(exams, 12)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    # for progress: if user logged in, get best score per exam
    progress_map = {}
    if request.user.is_authenticated:
        attempts = QuizAttempt.objects.filter(user=request.user, status="COMPLETED").values("exam_session").annotate(best=Avg("score"))
        for a in attempts:
            progress_map[a["exam_session"]] = a["best"]
    subjects = Subject.objects.annotate(c=Count("questions")).order_by("-c")[:12]
    return render(request, "exams/list.html", {"exams": page_obj, "q": q, "subjects": subjects, "progress_map": progress_map, "sort": sort, "status_filter": status_filter})

def get_exam_by_slug_or_route(slug):
    # Try slug exact, then route_id exact, then case-insensitive
    from django.shortcuts import get_object_or_404
    try:
        return ExamSession.objects.select_related("exam_family").get(slug=slug)
    except ExamSession.DoesNotExist:
        try:
            return ExamSession.objects.select_related("exam_family").get(route_id=slug)
        except ExamSession.DoesNotExist:
            # case-insensitive fallback
            return get_object_or_404(ExamSession.objects.select_related("exam_family"), Q(slug__iexact=slug) | Q(route_id__iexact=slug))

def exam_detail(request, slug):
    exam = get_exam_by_slug_or_route(slug)
    # subjects breakdown
    subjects = Subject.objects.filter(questions__exam_session=exam).annotate(qcount=Count("questions")).order_by("-qcount")
    # previous attempts for user
    attempts = []
    best_score = None
    avg_score = None
    if request.user.is_authenticated:
        attempts = QuizAttempt.objects.filter(user=request.user, exam_session=exam, status="COMPLETED").order_by("-started_at")[:5]
        if attempts:
            best_score = max(a.score for a in attempts)
            avg_score = sum(a.score for a in attempts)/len(attempts)
    # related exams
    related = ExamSession.objects.filter(exam_family=exam.exam_family).exclude(pk=exam.pk).order_by("-exam_date")[:3]
    total_qs = exam.questions.count()
    return render(request, "exams/detail.html", {"exam": exam, "subjects": subjects, "attempts": attempts, "best_score": best_score, "avg_score": avg_score, "related": related, "total_qs": total_qs})

def exam_subjects(request, slug):
    exam = get_exam_by_slug_or_route(slug)
    subjects = Subject.objects.filter(questions__exam_session=exam).annotate(qcount=Count("questions"))
    return render(request, "exams/subjects.html", {"exam": exam, "subjects": subjects})
