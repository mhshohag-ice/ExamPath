from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Q
from django.contrib.auth.models import User
from exams.models import ExamSession
from questions.models import Question, Subject
from quiz.models import QuizAttempt, UserAnswer
from imports_app.models import QuestionImport

@staff_member_required
def admin_dashboard(request):
    total_questions = Question.objects.count()
    total_sessions = ExamSession.objects.count()
    total_users = User.objects.count()
    total_attempts = QuizAttempt.objects.count()
    total_answered = UserAnswer.objects.count()
    # Most attempted questions
    most_attempted = Question.objects.annotate(attempts=Count('user_answers')).order_by('-attempts')[:5]
    # Hardest: lowest accuracy where attempts >5 (compute in Python to avoid extra SQL)
    qs_with_stats = list(Question.objects.annotate(total=Count('user_answers'), correct=Count('user_answers', filter=Q(user_answers__is_correct=True))).filter(total__gte=5))
    for q in qs_with_stats:
        q.acc = (q.correct / q.total) if q.total else 0
    hardest = sorted(qs_with_stats, key=lambda x: x.acc)[:5]
    easiest = sorted(qs_with_stats, key=lambda x: x.acc, reverse=True)[:5]
    # Most incorrect: highest incorrect count
    most_incorrect = Question.objects.annotate(incorrect=Count('user_answers', filter=Q(user_answers__is_correct=False))).order_by('-incorrect')[:5]
    # Popular exams: by attempts
    popular_exams = ExamSession.objects.annotate(attempts_count=Count('attempts')).order_by('-attempts_count')[:5]
    # Active users: by attempts
    active_users = User.objects.annotate(attempts_count=Count('quiz_attempts')).order_by('-attempts_count')[:5]
    # Daily questions answered: last 7 days
    from django.utils import timezone
    from datetime import timedelta
    daily = []
    for i in range(6,-1,-1):
        d = timezone.localdate() - timedelta(days=i)
        cnt = UserAnswer.objects.filter(answered_at__date=d).count()
        daily.append((d.strftime("%a %m/%d"), cnt))
    # Data quality
    missing_answers = Question.objects.filter(normalized_answer__isnull=True).count()
    missing_expl = Question.objects.filter(has_explanation=False).count()
    duplicates = QuestionImport.objects.aggregate(total=Count('duplicates_entries'))  # not directly
    # Use QuestionImportDuplicate count
    from imports_app.models import QuestionImportDuplicate
    dup_candidates = QuestionImportDuplicate.objects.count()
    # Imports
    recent_imports = QuestionImport.objects.order_by('-created_at')[:5]
    return render(request, 'admin_dashboard.html', {
        'total_questions': total_questions,
        'total_sessions': total_sessions,
        'total_users': total_users,
        'total_attempts': total_attempts,
        'total_answered': total_answered,
        'most_attempted': most_attempted,
        'hardest': hardest,
        'easiest': easiest,
        'most_incorrect': most_incorrect,
        'popular_exams': popular_exams,
        'active_users': active_users,
        'daily': daily,
        'missing_answers': missing_answers,
        'missing_expl': missing_expl,
        'dup_candidates': dup_candidates,
        'recent_imports': recent_imports,
    })
