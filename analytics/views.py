
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from quiz.models import QuizAttempt, UserAnswer
from questions.models import Subject
from .models import UserSubjectPerformance

@login_required
def analytics_dashboard(request):
    user = request.user
    # Overall metrics
    total_attempts = QuizAttempt.objects.filter(user=user, status="COMPLETED").count()
    total_questions = UserAnswer.objects.filter(attempt__user=user).count()
    correct = UserAnswer.objects.filter(attempt__user=user, is_correct=True).count()
    accuracy = round((correct/total_questions*100) if total_questions else 0,1)
    avg_time = UserAnswer.objects.filter(attempt__user=user).aggregate(avg=Avg("time_taken_seconds"))["avg"] or 0
    # XP
    total_xp = user.profile.xp_total
    # Exams completed
    exams_completed = QuizAttempt.objects.filter(user=user, mode="EXAM", status="COMPLETED").count()
    best_score = QuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("-score").first()
    # Accuracy over time: last 10 attempts
    recent_qs = QuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("-completed_at").values_list("score","completed_at")[:10]
    recent = list(reversed(list(recent_qs)))
    # Questions per day: last 7 days
    per_day = []
    today = timezone.localdate()
    for i in range(6,-1,-1):
        d = today - timedelta(days=i)
        cnt = UserAnswer.objects.filter(attempt__user=user, answered_at__date=d).count()
        per_day.append({"date": d.strftime("%a"), "count": cnt})
    # Subject performance
    subjects = UserSubjectPerformance.objects.filter(user=user).select_related("subject").order_by("-accuracy")
    # If no performance yet, calculate from UserAnswer
    if not subjects.exists():
        # Build from answers
        from django.db.models import Count
        subs = Subject.objects.filter(questions__user_answers__attempt__user=user).annotate(total=Count("questions__user_answers"), corr=Count("questions__user_answers", filter=Q(questions__user_answers__is_correct=True))).distinct()
        subjects = []
        for s in subs:
            acc = (s.corr/s.total*100) if s.total else 0
            subjects.append({"subject": s, "accuracy": round(acc,1), "attempted": s.total})
    # Weak areas
    weak = sorted(list(subjects), key=lambda x: x.accuracy if hasattr(x,"accuracy") else x["accuracy"])[:3] if subjects else []
    # Improvement graph data: score improvement
    improvement = list(QuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("started_at").values_list("score", flat=True))
    return render(request, "analytics/dashboard.html", {
        "total_attempts": total_attempts,
        "total_questions": total_questions,
        "correct": correct,
        "accuracy": accuracy,
        "avg_time": round(avg_time,1),
        "total_xp": total_xp,
        "exams_completed": exams_completed,
        "best_score": best_score.score if best_score else 0,
        "recent": recent,
        "per_day": per_day,
        "subjects": subjects,
        "weak": weak,
        "improvement": improvement,
    })
