from django.test import TestCase
from exams.models import ExamFamily, ExamSession
from questions.models import Subject, Question, Choice
from django.contrib.auth.models import User

class QuestionTests(TestCase):
    def setUp(self):
        fam = ExamFamily.objects.create(name="BCS", slug="bcs")
        self.sess = ExamSession.objects.create(exam_family=fam, name="50th BCS", slug="50th-bcs", route_id="50th-bcs", exam_type="General")
        self.subj = Subject.objects.create(name="Mental Ability", slug="mental-ability", code="MENTAL-ABILITY")

    def test_bengali_preserved(self):
        text = "জারিনের জন্ম ২৯ ফেব্রুয়ারী"
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=1, question_text=text, source_answer="b", normalized_answer="B", source_hash="h1")
        q.refresh_from_db()
        self.assertEqual(q.question_text, text)

    def test_latex_preserved(self):
        text = "Value is \\(\\frac{3}{11}\\) and display $$x^2$$"
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=2, question_text=text, source_answer="a", normalized_answer="A", source_hash="h2")
        self.assertIn("\\frac", q.question_text)

    def test_blank_answer_handling(self):
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=3, question_text="Blank?", source_answer="Blank", normalized_answer=None, is_resolved=False, source_hash="h3")
        self.assertIsNone(q.normalized_answer)
        self.assertFalse(q.is_resolved)

    def test_choice_correct_flag(self):
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=4, question_text="Q?", source_answer="c", normalized_answer="C", source_hash="h4")
        for label in ["A","B","C","D"]:
            Choice.objects.create(question=q, label=label, text=f"{label}", is_correct=(label=="C"))
        self.assertEqual(q.choices.filter(is_correct=True).first().label, "C")

    def test_question_list_view(self):
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=5, question_text="Searchable?", source_answer="a", normalized_answer="A", source_hash="h5")
        Choice.objects.create(question=q, label="A", text="A")
        resp = self.client.get('/questions/')
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get('/questions/?q=Searchable')
        self.assertEqual(resp2.status_code, 200)

    def test_question_detail_bengali(self):
        text = "জারিনের জন্ম"
        q = Question.objects.create(exam_session=self.sess, subject=self.subj, question_number=6, question_text=text, source_answer="a", normalized_answer="A", source_hash="h6")
        Choice.objects.create(question=q, label="A", text="২০০৪")
        resp = self.client.get(f'/questions/{q.id}/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "জারিন")
