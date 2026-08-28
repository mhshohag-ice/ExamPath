from django.shortcuts import render
from django.db.models import Count, Avg, Q
from django.contrib.auth.models import User
from exams.models import ExamSession, ExamFamily
from questions.models import Question, Subject

def landing(request):
    total_questions = Question.objects.filter(active=True).count()
    total_sessions = ExamSession.objects.count()
    total_subjects = Subject.objects.count()
    # Featured exams: latest 6 general
    featured = ExamSession.objects.select_related('exam_family').filter(status__in=['ACTIVE','DEMO']).order_by('-exam_date')[:6]
    # Recent activity for logged in? Use quiz attempts?
    recent_sessions = ExamSession.objects.order_by('-created_at')[:4]
    # Stats for hero
    # Calculate subjects for preview
    subjects = Subject.objects.annotate(qcount=Count('questions')).order_by('-qcount')[:8]
    context = {
        'total_questions': total_questions,
        'total_sessions': total_sessions,
        'total_subjects': total_subjects,
        'featured_exams': featured,
        'subjects': subjects,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'core/landing.html', context)

def search(request):
    q = request.GET.get('q','').strip()
    results = {'q': q, 'exams': [], 'questions': [], 'subjects': []}
    if q:
        results['exams'] = ExamSession.objects.filter(Q(name__icontains=q) | Q(route_id__icontains=q) | Q(exam_type__icontains=q))[:10]
        results['questions'] = Question.objects.filter(Q(question_text__icontains=q) | Q(explanation__icontains=q)).select_related('exam_session','subject')[:20]
        results['subjects'] = Subject.objects.filter(Q(name__icontains=q) | Q(code__icontains=q))[:10]
    return render(request, 'core/search.html', results)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler500(request):
    return render(request, 'errors/500.html', status=500)
