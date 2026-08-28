
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from exams.models import ExamSession
from questions.models import Question, Subject
from quiz.models import QuizAttempt, UserAnswer, QuestionReview
from bookmarks.models import Bookmark
from accounts.models import DailyActivity
from gamification.models import Level, UserAchievement

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    # Level progress
    total_xp = profile.xp_total
    # Find next level threshold
    try:
        current_level = Level.objects.filter(number=profile.level).first()
        next_level = Level.objects.filter(number=profile.level+1).first()
        if next_level:
            xp_needed = next_level.xp_threshold - total_xp
            xp_prev = current_level.xp_threshold if current_level else 0
            xp_range = next_level.xp_threshold - xp_prev
            progress = int(((total_xp - xp_prev)/xp_range)*100) if xp_range else 100
        else:
            xp_needed = 0
            progress = 100
    except:
        progress = 50
        xp_needed = 100
        next_level = None
    # Today's goal: 50 questions (configurable)
    today = timezone.localdate()
    daily = DailyActivity.objects.filter(user=user, date=today).first()
    today_answered = daily.questions_answered if daily else 0
    today_goal = 50
    # Accuracy
    recent = QuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("-started_at")[:10]
    accuracy = round(sum(a.score for a in recent)/len(recent),1) if recent else 0
    # Continue learning: unfinished attempt
    unfinished = QuizAttempt.objects.filter(user=user, status="IN_PROGRESS").order_by("-started_at").first()
    continue_data = None
    if unfinished:
        answered = unfinished.answers.filter(selected_label__isnull=False).exclude(selected_label="").count()
        total = unfinished.total_questions or 1
        pct = int((answered/total)*100)
        continue_data = {"attempt": unfinished, "answered": answered, "total": total, "pct": pct}
    # Daily challenge: 10 questions, 5 minutes, +100 XP
    daily_challenge_questions = 10
    # Recent activity feed
    recent_attempts = QuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("-completed_at")[:5]
    achievements = UserAchievement.objects.filter(user=user).select_related("achievement").order_by("-unlocked_at")[:3]
    # Weak areas: lowest accuracy subjects
    from analytics.models import UserSubjectPerformance
    weak = UserSubjectPerformance.objects.filter(user=user).order_by("accuracy")[:3]
    # Bookmarks count
    bookmarks_count = Bookmark.objects.filter(user=user).count()
    # Streak calendar: last 7 days
    streak_days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        act = DailyActivity.objects.filter(user=user, date=d).first()
        streak_days.append({"date": d, "active": bool(act and act.questions_answered>0), "is_today": d==today})
    # Level info
    return render(request, "dashboard/dashboard.html", {
        "profile": profile,
        "progress": progress,
        "xp_needed": xp_needed,
        "next_level": next_level,
        "today_answered": today_answered,
        "today_goal": today_goal,
        "accuracy": accuracy,
        "continue_data": continue_data,
        "recent_attempts": recent_attempts,
        "achievements": achievements,
        "weak": weak,
        "bookmarks_count": bookmarks_count,
        "streak_days": streak_days,
    })
