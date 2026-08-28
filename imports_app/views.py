
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import QuestionImport
from .parser import parse_markdown_file, validate_parsed_data
from .services import import_parsed_data
import pathlib, hashlib, tempfile, os

@staff_member_required
def import_upload(request):
    if request.method == "POST" and request.FILES.get("file"):
        f = request.FILES["file"]
        # save temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
            for chunk in f.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
        file_hash = hashlib.sha256(open(tmp_path,"rb").read()).hexdigest()
        import_job = QuestionImport.objects.create(filename=f.name, file_path=tmp_path, file_hash=file_hash, status="PROCESSING", created_by=request.user)
        try:
            parsed = parse_markdown_file(tmp_path)
            validation = validate_parsed_data(parsed)
            result = import_parsed_data(parsed, import_job, preview=True)
            request.session["import_preview"] = {"job_id": import_job.id, "stats": parsed["stats"], "warnings": validation["warnings"][:20], "errors": validation["errors"][:20], "preview": result}
            messages.success(request, f"Parsed {parsed['stats']['total_mcq_questions']} MCQ + {parsed['stats']['total_written_questions']} Written. Ready for approval.")
            return redirect("import_preview", job_id=import_job.id)
        except Exception as e:
            import_job.status="FAILED"
            import_job.report={"error": str(e)}
            import_job.save()
            messages.error(request, f"Parse failed: {e}")
            return redirect("import_upload")
    jobs = QuestionImport.objects.order_by("-created_at")[:10]
    return render(request, "imports_app/upload.html", {"jobs": jobs})

@staff_member_required
def import_preview(request, job_id):
    job = QuestionImport.objects.get(id=job_id)
    warnings = job.warnings.all()[:20] if hasattr(job,"warnings") else []
    errors = job.errors.all()[:20] if hasattr(job,"errors") else []
    dups = job.duplicates_entries.all()[:20] if hasattr(job,"duplicates_entries") else []
    return render(request, "imports_app/preview.html", {"job": job, "warnings": warnings, "errors": errors, "dups": dups})

@staff_member_required
def import_approve(request, job_id):
    job = QuestionImport.objects.get(id=job_id)
    if request.method == "POST":
        # Retrieve temp file and parse again for actual import
        tmp_path = job.file_path
        if not pathlib.Path(tmp_path).exists():
            messages.error(request, "Temp file missing. Please re-upload.")
            return redirect("import_upload")
        from .parser import parse_markdown_file
        from .services import import_parsed_data
        parsed = parse_markdown_file(tmp_path)
        result = import_parsed_data(parsed, job, preview=False)
        messages.success(request, f"Imported {result['imported']} questions")
        return redirect("import_preview", job_id=job.id)
    return render(request, "imports_app/approve.html", {"job": job})
