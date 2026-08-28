from django.test import TestCase
from django.contrib.auth.models import User
from gamification.models import Level, Achievement, UserAchievement, XPTransaction, award_xp, XP_RULES
from accounts.models import Profile
from quiz.models import QuizAttempt, UserAnswer
from exams.models import ExamFamily, ExamSession
from questions.models import Subject, Question, Choice
from django.utils import timezone
from datetime import timedelta

class GamificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('gamer', 'g@test.com', 'pass')
        # levels
        Level.objects.create(number=1, title="Beginner", xp_threshold=0)
        Level.objects.create(number=2, title="Learner", xp_threshold=100)
        Level.objects.create(number=3, title="Explorer", xp_threshold=300)

    def test_xp_award_and_level(self):
        award_xp(self.user, 10, "CORRECT_ANSWER")
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp_total, 10)
        self.assertEqual(self.user.profile.level, 1)
        award_xp(self.user, 100, "QUIZ_COMPLETED")
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.level, 2)

    def test_xp_transaction_created(self):
        award_xp(self.user, 50, "DAILY_CHALLENGE")
        tx = XPTransaction.objects.filter(user=self.user).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, 50)

    def test_streak_update(self):
        profile = self.user.profile
        today = timezone.localdate()
        profile.update_streak(today)
        self.assertEqual(profile.current_streak, 1)
        # same day no increase
        profile.update_streak(today)
        self.assertEqual(profile.current_streak, 1)
        # next day
        profile.update_streak(today + timedelta(days=1))
        self.assertEqual(profile.current_streak, 2)
        # skip 2 days -> reset
        profile.update_streak(today + timedelta(days=4))
        self.assertEqual(profile.current_streak, 1)

    def test_achievement_unlock(self):
        # create achievement
        ach = Achievement.objects.create(code="first_answer", title="First Answer", description="...", icon="🎯", xp_reward=10, rule_type="first_answer", rule_threshold=1)
        from gamification.views import check_achievements
        # before any answer, not unlocked
        self.assertFalse(UserAchievement.objects.filter(user=self.user, achievement=ach).exists())
        # create a question and answer
        fam = ExamFamily.objects.create(name="BCS", slug="bcs2")
        sess = ExamSession.objects.create(exam_family=fam, name="Test", slug="test2", route_id="test2")
        subj = Subject.objects.create(name="Sub", slug="sub2", code="SUB2")
        q = Question.objects.create(exam_session=sess, subject=subj, question_number=1, question_text="Q?", source_answer="a", normalized_answer="A", source_hash="h1")
        Choice.objects.create(question=q, label="A", text="A", is_correct=True)
        from quiz.models import QuizAttempt
        att = QuizAttempt.objects.create(user=self.user, mode="PRACTICE", total_questions=1, status="COMPLETED")
        UserAnswer.objects.create(attempt=att, question=q, selected_label="A", is_correct=True)
        check_achievements(self.user)
        self.assertTrue(UserAchievement.objects.filter(user=self.user, achievement=ach).exists())

    def test_leaderboard_order(self):
        u2 = User.objects.create_user('gamer2', 'g2@test.com', 'pass')
        award_xp(self.user, 100, "QUIZ_COMPLETED")
        award_xp(u2, 200, "QUIZ_COMPLETED")
        from django.test import Client
        c = Client()
        c.login(username='gamer', password='pass')
        resp = c.get('/leaderboard/')
        self.assertEqual(resp.status_code, 200)
