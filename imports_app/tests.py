from django.test import TestCase
from pathlib import Path
import tempfile, hashlib
from imports_app.parser import parse_markdown_file, normalize_answer, hash_question, validate_parsed_data
from imports_app.services import import_parsed_data
from imports_app.models import QuestionImport
from exams.models import ExamSession
from questions.models import Question

class ParserTests(TestCase):
    def test_normalize_answer(self):
        self.assertEqual(normalize_answer("a"), "A")
        self.assertEqual(normalize_answer("b"), "B")
        self.assertIsNone(normalize_answer("Blank"))
        self.assertIsNone(normalize_answer(""))
        self.assertIsNone(normalize_answer("  "))

    def test_hash_question(self):
        h1 = hash_question("  Hello   World ")
        h2 = hash_question("hello world")
        self.assertEqual(h1, h2)

    def test_parse_sample_mcq(self):
        sample = '''
### 1. 50th BCS - General (2026-01-30)

- **Route ID:** `50th-bcs`
- **Type:** General | **Date:** 2026-01-30 | **Marks:** Marks 200
- **Questions:** 200

#### Question 1 [MENTAL-ABILITY] - Answer: `b`

**Q:** জারিনের জন্ম ২৯ ফেব্রুয়ারী।

- **A.** ২০০২
- **B.** ২০০৪ ✅
- **C.** ২০০৬
- **D.** ২০১০

<details><summary>💡 Explanation</summary>

Explanation here

</details>
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(sample)
            path = f.name
        parsed = parse_markdown_file(path)
        self.assertEqual(len(parsed['exam_sessions']), 1)
        es = parsed['exam_sessions'][0]
        self.assertEqual(es.route_id, '50th-bcs')
        self.assertEqual(len(es.questions), 1)
        q = es.questions[0]
        self.assertEqual(q.question_number, 1)
        self.assertEqual(q.category, "MENTAL-ABILITY")
        self.assertEqual(q.normalized_answer, "B")
        self.assertEqual(len(q.choices), 4)
        self.assertTrue(q.has_explanation)
        self.assertIn("জারিন", q.question_text)

    def test_parse_blank_answer(self):
        sample = '''
### 1. Demo - General (2025-01-05)

- **Route ID:** `D-M`
- **Type:** General | **Date:** 2025-01-05 | **Marks:** Marks 20
- **Questions:** 20

#### Question 1 [BANGLA-LANGUAGE] - Answer: `Blank`

**Q:** Blank question?

- **A.** A
- **B.** B
- **C.** C
- **D.** D

<details><summary>💡 Explanation</summary>Exp</details>
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(sample)
            path = f.name
        parsed = parse_markdown_file(path)
        q = parsed['exam_sessions'][0].questions[0]
        self.assertIsNone(q.normalized_answer)
        self.assertEqual(q.source_answer, "Blank")

    def test_malformed_and_duplicate_detection(self):
        sample = '''
### 1. 50th BCS - General (2026-01-30)

- **Route ID:** `50th-bcs`
- **Type:** General | **Date:** 2026-01-30 | **Marks:** Marks 200
- **Questions:** 200

#### Question 1 [MENTAL-ABILITY] - Answer: `a`

**Q:** Q1?

- **A.** A
- **B.** B
- **C.** C
- **D.** D

<details><summary>💡 Explanation</summary>Exp</details>

#### Question 2 [MENTAL-ABILITY] - Answer: `a`

**Q:** Q1?

- **A.** A
- **B.** B
- **C.** C
- **D.** D

<details><summary>💡 Explanation</summary>Exp</details>
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(sample)
            path = f.name
        parsed = parse_markdown_file(path)
        self.assertEqual(len(parsed['exam_sessions'][0].questions), 2)
        # hashes same -> duplicate
        h1 = hash_question(parsed['exam_sessions'][0].questions[0].question_text)
        h2 = hash_question(parsed['exam_sessions'][0].questions[1].question_text)
        self.assertEqual(h1, h2)

    def test_import_idempotency(self):
        sample = '''
### 1. Demo - General (2025-01-05)

- **Route ID:** `D-M`
- **Type:** General | **Date:** 2025-01-05 | **Marks:** Marks 20
- **Questions:** 2

#### Question 1 [TEST] - Answer: `a`

**Q:** Q1?

- **A.** A
- **B.** B
- **C.** C
- **D.** D

<details><summary>💡 Explanation</summary>Exp</details>

#### Question 2 [TEST] - Answer: `b`

**Q:** Q2?

- **A.** A
- **B.** B
- **C.** C
- **D.** D

<details><summary>💡 Explanation</summary>Exp</details>
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(sample)
            path = f.name
        parsed = parse_markdown_file(path)
        import_job = QuestionImport.objects.create(filename="test.md", file_path=path, file_hash="abc", status="PROCESSING")
        result1 = import_parsed_data(parsed, import_job, preview=False)
        self.assertEqual(result1['imported'], 2)
        # second import same file should be idempotent
        import_job2 = QuestionImport.objects.create(filename="test.md", file_path=path, file_hash="abc2", status="PROCESSING")
        result2 = import_parsed_data(parsed, import_job2, preview=False)
        self.assertEqual(result2['imported'], 0)
        self.assertEqual(result2['skipped'], 2)

class FullFileParseTests(TestCase):
    def test_full_file_stats(self):
        path = Path(r'I:\Other computers\My Laptop\Desktop\Uttoron\Uttoron_Question_Bank_All.md')
        if not path.exists():
            self.skipTest("Full file not found")
        parsed = parse_markdown_file(str(path))
        self.assertGreaterEqual(len(parsed['exam_sessions']), 47)
        self.assertGreaterEqual(parsed['stats']['total_mcq_questions'], 5000)
        validation = validate_parsed_data(parsed)
        # should have some warnings but not crash
        self.assertIsInstance(validation['warnings'], list)
