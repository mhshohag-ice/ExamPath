
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Level, Achievement, UserAchievement, XPTransaction, LeaderboardSnapshot
from django.utils import timezone
from datetime import timedelta

def check_achievements(user):
    # Rule-driven achievement unlocking
    from quiz.models import QuizAttempt, UserAnswer
    from bookmarks.models import Bookmark
    achievements = Achievement.objects.filter(is_active=True)
    unlocked_codes = set(UserAchievement.objects.filter(user=user).values_list("achievement__code", flat=True))
    for ach in achievements:
        if ach.code in unlocked_codes:
            continue
        unlocked = False
        if ach.rule_type == "first_answer":
            if UserAnswer.objects.filter(attempt__user=user).exists():
                unlocked = True
        elif ach.rule_type == "first_exam":
            if QuizAttempt.objects.filter(user=user, status="COMPLETED").exists():
                unlocked = True
        elif ach.rule_type == "questions_answered":
            count = UserAnswer.objects.filter(attempt__user=user).count()
            if count >= ach.rule_threshold:
                unlocked = True
        elif ach.rule_type == "perfect_quiz":
            if QuizAttempt.objects.filter(user=user, score=100).exists():
                unlocked = True
        elif ach.rule_type == "streak":
            if user.profile.current_streak >= ach.rule_threshold:
                unlocked = True
        elif ach.rule_type == "exam_master":
            if QuizAttempt.objects.filter(user=user, mode="EXAM", status="COMPLETED").exists():
                unlocked = True
        elif ach.rule_type == "subject_master":
            from analytics.models import UserSubjectPerformance
            if UserSubjectPerformance.objects.filter(user=user, accuracy__gte=90).exists():
                unlocked = True
        if unlocked:
            UserAchievement.objects.create(user=user, achievement=ach, xp_awarded=ach.xp_reward)
            if ach.xp_reward:
                from .models import award_xp
                award_xp(user, ach.xp_reward, "ACHIEVEMENT", reference_type="Achievement", reference_id=ach.id, description=ach.title)

@login_required
def achievements_view(request):
    all_ach = Achievement.objects.filter(is_active=True).order_by("display_order")
    user_ach = {ua.achievement_id: ua for ua in UserAchievement.objects.filter(user=request.user).select_related("achievement")}
    return render(request, "gamification/achievements.html", {"achievements": all_ach, "user_ach": user_ach})

def leaderboard_view(request):
    from django.db.models import Sum
    period = request.GET.get("period","all")
    # Global leaderboard by total XP
    # For weekly/monthly, filter XPTransactions by date
    users = User.objects.all()
    leaderboard = []
    now = timezone.now()
    if period == "weekly":
        start = now - timedelta(days=7)
        xp_data = XPTransaction.objects.filter(created_at__gte=start).values("user").annotate(total=Sum("amount")).order_by("-total")[:50]
    elif period == "monthly":
        start = now - timedelta(days=30)
        xp_data = XPTransaction.objects.filter(created_at__gte=start).values("user").annotate(total=Sum("amount")).order_by("-total")[:50]
    else:
        # all time: use profile xp_total
        xp_data = User.objects.filter(profile__xp_total__gt=0).values("id","username","profile__xp_total","profile__level").order_by("-profile__xp_total")[:50]
        # Normalize
        normalized = []
        for idx, u in enumerate(xp_data, start=1):
            normalized.append({"user_id": u["id"], "username": u["username"], "total": u["profile__xp_total"], "rank": idx, "level": u["profile__level"]})
        # Add current user's rank if not in top 50
        if request.user.is_authenticated:
            user_rank = User.objects.filter(profile__xp_total__gt=request.user.profile.xp_total).count() + 1
            leaderboard = normalized
            # ensure user visible
            if not any(x["user_id"]==request.user.id for x in normalized):
                leaderboard.append({"user_id": request.user.id, "username": request.user.username, "total": request.user.profile.xp_total, "rank": user_rank, "level": request.user.profile.level, "is_you": True})
            else:
                for x in leaderboard:
                    if x["user_id"]==request.user.id:
                        x["is_you"]=True
            return render(request, "gamification/leaderboard.html", {"leaderboard": leaderboard, "period": period, "user_rank": user_rank})
        return render(request, "gamification/leaderboard.html", {"leaderboard": normalized, "period": period})
    # For weekly/monthly, build leaderboard from xp_data
    leaderboard = []
    for idx, entry in enumerate(xp_data, start=1):
        try:
            u = User.objects.get(id=entry["user"])
            leaderboard.append({"user_id": u.id, "username": u.username, "total": entry["total"], "rank": idx, "level": u.profile.level})
        except: continue
    # Ensure current user visible for period
    if request.user.is_authenticated and period != "all":
        # find user's total for period
        user_total = XPTransaction.objects.filter(user=request.user, created_at__gte=start).aggregate(s=Sum("amount"))["s"] or 0
        user_rank = 1 + XPTransaction.objects.filter(created_at__gte=start).values("user").annotate(total=Sum("amount")).filter(total__gt=user_total).count()
        if not any(x["user_id"]==request.user.id for x in leaderboard):
            leaderboard.append({"user_id": request.user.id, "username": request.user.username, "total": user_total, "rank": user_rank, "level": request.user.profile.level, "is_you": True})
        else:
            for x in leaderboard:
                if x["user_id"]==request.user.id:
                    x["is_you"]=True
        return render(request, "gamification/leaderboard.html", {"leaderboard": leaderboard, "period": period, "user_rank": user_rank})
    return render(request, "gamification/leaderboard.html", {"leaderboard": leaderboard, "period": period})

@login_required
def xp_history(request):
    txs = XPTransaction.objects.filter(user=request.user).order_by("-created_at")[:50]
    return render(request, "gamification/xp_history.html", {"txs": txs})
