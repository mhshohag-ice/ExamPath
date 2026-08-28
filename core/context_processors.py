from django.db.models import Count, Sum
from django.contrib.auth.models import User

def site_stats(request):
    try:
        from exams.models import ExamSession
        from questions.models import Question
        total_questions = Question.objects.filter(active=True).count()
        total_sessions = ExamSession.objects.count()
        total_users = User.objects.count()
    except Exception:
        total_questions = 0
        total_sessions = 0
        total_users = 0
    return {
        'site_total_questions': total_questions,
        'site_total_sessions': total_sessions,
        'site_total_users': total_users,
    }

def gamification_context(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            return {
                'user_xp': profile.xp_total,
                'user_level': profile.level,
                'user_streak': profile.current_streak,
            }
        except Exception:
            pass
    return {}
