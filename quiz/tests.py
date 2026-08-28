from django.test import TestCase, Client
from django.contrib.auth.models import User
from exams.models import ExamFamily, ExamSession
from questions.models import Subject, Question, Choice
from quiz.models import QuizAttempt, UserAnswer
import json

class QuizTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 't@test.com', 'pass123')
        self.client.login(username='tester', password='pass123')
        fam = ExamFamily.objects.create(name="BCS", slug="bcs")
        self.sess = ExamSession.objects.create(exam_family=fam, name="50th BCS", slug="50th-bcs", route_id="50th-bcs", exam_type="General", marks=100)
        self.subj = Subject.objects.create(name="Test Subj", slug="test-subj", code="TEST")
        self.questions = []
        for i in range(1,11):
            q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=i, question_text=f"Q{i}?", source_answer="a", normalized_answer="A", source_hash=f"hash{i}")
            for label in ["A","B","C","D"]:
                Choice.objects.create(question=q, label=label, text=f"{label}", is_correct=(label=="A"))
            self.questions.append(q)

    def test_practice_quiz_flow(self):
        # start quiz
        resp = self.client.get('/quiz/start/50th-bcs/?mode=PRACTICE&count=5')
        self.assertEqual(resp.status_code, 302)
        attempt_id = int(resp['Location'].split('/')[2])
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertEqual(attempt.total_questions, 5)
        # answer all correctly
        qids = self.client.session.get(f'attempt_{attempt_id}_qids')
        self.assertIsNotNone(qids)
        for qid in qids:
            q = Question.objects.get(id=qid)
            r = self.client.post(f'/quiz/{attempt_id}/answer/', data=json.dumps({'question_id': qid, 'choice': 'A'}), content_type='application/json')
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.json()['is_correct'])
        # submit
        r2 = self.client.get(f'/quiz/{attempt_id}/submit/')
        self.assertEqual(r2.status_code, 302)
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, 'COMPLETED')
        self.assertEqual(attempt.score, 100.0)
        self.assertEqual(attempt.correct_count, 5)

    def test_skipped_handling(self):
        resp = self.client.get('/quiz/start/50th-bcs/?mode=PRACTICE&count=5')
        attempt_id = int(resp['Location'].split('/')[2])
        qids = self.client.session.get(f'attempt_{attempt_id}_qids')
        # answer only 2
        for qid in qids[:2]:
            self.client.post(f'/quiz/{attempt_id}/answer/', data=json.dumps({'question_id': qid, 'choice': 'A'}), content_type='application/json')
        # submit with skips
        self.client.get(f'/quiz/{attempt_id}/submit/')
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertEqual(attempt.correct_count, 2)
        self.assertEqual(attempt.skipped_count, 3)

    def test_incorrect_handling(self):
        resp = self.client.get('/quiz/start/50th-bcs/?mode=PRACTICE&count=5')
        attempt_id = int(resp['Location'].split('/')[2])
        qids = self.client.session.get(f'attempt_{attempt_id}_qids')
        for qid in qids:
            self.client.post(f'/quiz/{attempt_id}/answer/', data=json.dumps({'question_id': qid, 'choice': 'B'}), content_type='application/json')
        self.client.get(f'/quiz/{attempt_id}/submit/')
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertEqual(attempt.incorrect_count, 5)
        self.assertEqual(attempt.score, 0)

    def test_exam_simulation(self):
        resp = self.client.get(f'/quiz/exam/50th-bcs/')
        self.assertEqual(resp.status_code, 302)
        attempt_id = int(resp['Location'].split('/')[2])
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertEqual(attempt.mode, 'EXAM')
        self.assertEqual(attempt.total_questions, 10)

    def test_auto_save_and_resume(self):
        resp = self.client.get('/quiz/start/50th-bcs/?mode=PRACTICE&count=5')
        attempt_id = int(resp['Location'].split('/')[2])
        # take page should show resume
        r = self.client.get(f'/quiz/{attempt_id}/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Navigator")

    def test_random_selection_efficiency(self):
        # should not use order_by("?") for large selection; test that _select_questions_for_attempt returns correct count without error
        from quiz.views import _select_questions_for_attempt
        qs = _select_questions_for_attempt(self.user, "PRACTICE", exam=self.sess, count=5)
        self.assertEqual(len(qs), 5)
