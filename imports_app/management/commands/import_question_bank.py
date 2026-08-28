import pathlib
import hashlib
import time
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from imports_app.parser import parse_markdown_file, validate_parsed_data
from imports_app.services import import_parsed_data
from imports_app.models import QuestionImport


class Command(BaseCommand):
    help = "Import BCS question bank from Markdown file"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="Path to Markdown file")
        parser.add_argument("--preview", action="store_true", help="Preview only, don't import")
        parser.add_argument("--approve", action="store_true", help="Auto-approve after preview (skip interactive)")
        parser.add_argument("--user", type=str, default=None, help="Username to attribute import to")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        preview_mode = options["preview"]
        approve = options["approve"]
        user = None
        if options["user"]:
            try:
                user = User.objects.get(username=options["user"])
            except User.DoesNotExist:
                self.stderr.write(f"User {options['user']} not found, using None")

        path = pathlib.Path(filepath)
        if not path.exists():
            # Try relative to base
            from django.conf import settings
            alt = settings.BASE_DIR / filepath
            if alt.exists():
                path = alt
            else:
                raise CommandError(f"File not found: {filepath}")

        # Compute file hash for idempotency
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()

        # Check existing import with same hash and completed
        existing = QuestionImport.objects.filter(file_hash=file_hash, status=QuestionImport.Status.COMPLETED).first()
        if existing:
            self.stdout.write(self.style.WARNING(f"File already imported previously (id={existing.id}, imported={existing.imported}). Running again will check idempotency (skip duplicates)."))

        import_job = QuestionImport.objects.create(
            filename=path.name,
            file_path=str(path),
            file_hash=file_hash,
            status=QuestionImport.Status.PROCESSING,
            created_by=user,
        )
        self.stdout.write(f"Parsing {path} ...")
        try:
            parsed = parse_markdown_file(str(path))
        except Exception as e:
            import_job.status = QuestionImport.Status.FAILED
            import_job.report = {"error": str(e)}
            import_job.save()
            raise CommandError(f"Parse failed: {e}")

        stats = parsed["stats"]
        self.stdout.write(self.style.SUCCESS(f"Parsed: {stats['total_exam_sessions']} exam sessions, {stats['total_mcq_questions']} MCQ, {stats['total_written_sessions']} written sessions, {stats['total_written_questions']} written Qs"))

        validation = validate_parsed_data(parsed)
        warnings = validation["warnings"]
        errors = validation["errors"]
        self.stdout.write(f"Validation: {len(warnings)} warnings, {len(errors)} errors")
        for w in warnings[:10]:
            self.stdout.write(self.style.WARNING(f" WARN: {w}"))
        for e in errors[:10]:
            self.stdout.write(self.style.ERROR(f" ERR: {e}"))

        if preview_mode:
            self.stdout.write(self.style.NOTICE("=== PREVIEW MODE ==="))
            result = import_parsed_data(parsed, import_job, preview=True)
            self.stdout.write(f"Preview: total {result['total']}, would import {result['total']}, duplicates {result['duplicates']}, invalid {result['invalid']}")
            import_job.status = QuestionImport.Status.PREVIEW
            import_job.total_records = result["total"]
            import_job.duplicates = result["duplicates"]
            import_job.invalid = result["invalid"]
            import_job.warnings_count = result["warnings"]
            import_job.errors_count = result["errors"]
            import_job.save()
            # Show report
            for es in result["report"]["exam_sessions"][:10]:
                self.stdout.write(f"  Exam {es['name']} route={es['route_id']} parsed={es['parsed']} declared={es['declared']}")
            self.stdout.write(self.style.SUCCESS("Preview complete. Use --approve or run without --preview to import."))
            return

        # If not preview, show preview summary and ask approval unless --approve
        if not approve:
            self.stdout.write(self.style.NOTICE("Import Preview:"))
            # Do a quick preview calculation without DB writes but show stats
            # For simplicity, just show parsed stats
            self.stdout.write(f" Exam Sessions Found: {stats['total_exam_sessions']}")
            self.stdout.write(f" Questions Found: {stats['total_mcq_questions'] + stats['total_written_questions']}")
            self.stdout.write(f" Warnings: {len(warnings)}")
            self.stdout.write(f" Errors: {len(errors)}")
            # In non-interactive, proceed
            self.stdout.write("Proceeding to import... (use --preview to see detailed preview)")

        self.stdout.write("Importing to database (idempotent)...")
        try:
            result = import_parsed_data(parsed, import_job, preview=False)
        except Exception as e:
            import_job.status = QuestionImport.Status.FAILED
            import_job.report = {"error": str(e)}
            import_job.save()
            import traceback
            traceback.print_exc()
            raise CommandError(f"Import failed: {e}")

        self.stdout.write(self.style.SUCCESS(f"Import Completed: imported={result['imported']}, skipped={result['skipped']}, duplicates={result['duplicates']}, invalid={result['invalid']}, warnings={result['warnings']}, errors={result['errors']}, time={result['processing_time']:.2f}s"))

        # Data quality report
        self.stdout.write(self.style.SUCCESS("\n=== Question Bank Health ==="))
        from questions.models import Question
        total_q = Question.objects.count()
        missing_answers = Question.objects.filter(normalized_answer__isnull=True).count()
        missing_expl = Question.objects.filter(has_explanation=False).count()
        total_choices = Question.objects.filter(active=True).count()
        self.stdout.write(f" Total Questions in DB: {total_q}")
        self.stdout.write(f" Missing Answers (unresolved): {missing_answers}")
        self.stdout.write(f" Missing Explanations: {missing_expl}")
        self.stdout.write(f" Duplicates flagged: {result['duplicates']}")
        # Check that duplicate detection via import job
        dup_candidates = import_job.duplicates_entries.count()
        self.stdout.write(f" Duplicate candidates stored: {dup_candidates}")

        # Source records vs parsed vs imported discrepancy check
        declared_total = sum(es.question_count_declared for es in parsed["exam_sessions"]) + sum(ws.question_count_declared for ws in parsed["written_sessions"])
        self.stdout.write(f" Declared total (from markdown metadata): {declared_total}")
        self.stdout.write(f" Parsed total: {result['total']}")
        self.stdout.write(f" Imported new: {result['imported']}")
        if declared_total != result["total"]:
            self.stdout.write(self.style.WARNING(f" Discrepancy: declared {declared_total} != parsed {result['total']}. See warnings."))

        self.stdout.write(self.style.SUCCESS("Done."))
