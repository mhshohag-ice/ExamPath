from django.test import TestCase
from django.contrib.auth.models import User
from exams.models import ExamFamily, ExamSession
from questions.models import Subject, Question, Choice

class ExamModelTests(TestCase):
    def test_exam_hierarchy(self):
        fam = ExamFamily.objects.create(name="BCS", slug="bcs")
        sess = ExamSession.objects.create(exam_family=fam, name="50th BCS", slug="50th-bcs-test", route_id="50th-bcs-test", exam_type="General", marks=200)
        subj = Subject.objects.create(name="Mental Ability", slug="mental-ability", code="MENTAL-ABILITY")
        q = Question.objects.create(exam_session=sess, subject=subj, question_number=1, question_text="Test?", source_answer="a", normalized_answer="A", source_hash="abc")
        Choice.objects.create(question=q, label="A", text="Opt A", is_correct=True)
        Choice.objects.create(question=q, label="B", text="Opt B")
        self.assertEqual(sess.questions.count(), 1)
        self.assertEqual(q.choices.count(), 2)
        self.assertTrue(sess.exam_family.name == "BCS")

class ExamViewTests(TestCase):
    def setUp(self):
        fam = ExamFamily.objects.create(name="BCS", slug="bcs")
        self.sess = ExamSession.objects.create(exam_family=fam, name="50th BCS", slug="50th-bcs", route_id="50th-bcs", exam_type="General", marks=200, exam_date="2026-01-30")
        subj = Subject.objects.create(name="Mental Ability", slug="mental-ability", code="MENTAL-ABILITY")
        for i in range(1,6):
            q = Question.objects.create(exam_session=self.sess, subject=subj, question_number=i, question_text=f"Q{i}?", source_answer="a", normalized_answer="A", source_hash=f"hash{i}")
            for label in ["A","B","C","D"]:
                Choice.objects.create(question=q, label=label, text=f"{label} opt", is_correct=(label=="A"))

    def test_exam_list(self):
        resp = self.client.get('/exams/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "50th BCS")

    def test_exam_detail(self):
        resp = self.client.get(f'/exams/{self.sess.slug}/')
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get(f'/exams/{self.sess.route_id}/')
        self.assertEqual(resp2.status_code, 200)

    def test_exam_type_specialization(self):
        fam = ExamFamily.objects.get(slug="bcs")
        sess = ExamSession.objects.create(exam_family=fam, name="48th BCS", slug="48th-medical", route_id="48thBCS", exam_type="Special (Health) Medical Part", specialization="Medical", status="ACTIVE")
        self.assertEqual(sess.specialization, "Medical")
        self.assertIn("Medical", sess.display_name)
