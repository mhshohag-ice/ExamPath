import time, hashlib, re
from datetime import datetime
from django.db import transaction
from django.utils.text import slugify
from exams.models import ExamFamily, ExamSession
from questions.models import Subject, Question, Choice, WrittenQuestion
from imports_app.models import QuestionImport, QuestionImportError, QuestionImportWarning, QuestionImportDuplicate

def ensure_exam_family():
    return ExamFamily.objects.get_or_create(name="BCS", defaults={"slug":"bcs","description":"Bangladesh Civil Service","icon":"🎓","active":True})[0]

_subject_cache={}
def ensure_subject_cached(code_raw):
    if not code_raw or not code_raw.strip():
        code_raw="GENERAL"
    key=code_raw.strip()
    if key in _subject_cache:
        return _subject_cache[key]
    # normalize
    code_normalized=re.sub(r'\s+','-', key.upper())
    code_normalized=re.sub(r'[^A-Z0-9\-]','-', code_normalized)
    code_normalized=re.sub(r'-+','-', code_normalized).strip('-')
    if not code_normalized:
        code_normalized="GENERAL"
    pretty_map={"MENTAL-ABILITY":"Mental Ability","GENERAL-SCIENCE":"General Science","INTERNATIONAL-AFFAIRS":"International Affairs","COMPUTER-AND-INFORMATION-TECHNOLOGY":"Computer & IT","MATHEMATICAL-REASONING":"Mathematical Reasoning","BANGLA-LANGUAGE":"Bangla Language","BANGLADESH-AFFAIRS":"Bangladesh Affairs","BANGLA-LITERATURE":"Bangla Literature","ENGLISH-LANGUAGE":"English Language","ENGLISH-LITERATURE":"English Literature","ETHICS-VALUES-GOOD-GOVERNANCE":"Ethics & Governance","GEOGRAPHY-ENVIRONMENT-AND-DIGESTER-MANAGEMENT":"Geography & Environment","BANGLA":"Bangla","ANATOMY":"Anatomy","PHYSIOLOGY":"Physiology"}
    name=pretty_map.get(code_normalized, code_normalized.replace("-"," ").title())
    if any(ord(c)>127 for c in key):
        name=key
    subj,created=Subject.objects.get_or_create(code=code_normalized, defaults={"name":name,"slug":slugify(name) or slugify(code_normalized.lower()),"display_order":0})
    if not subj.slug:
        subj.slug=slugify(name) or slugify(code_normalized.lower())
        subj.save()
    _subject_cache[key]=subj
    _subject_cache[code_normalized]=subj
    return subj

def parse_date(date_str):
    if not date_str: return None
    date_str=date_str.strip()
    if date_str in ("???","????",""): return None
    if date_str.startswith("22021"): date_str=date_str.replace("22021","2021")
    for fmt in ("%Y-%m-%d","%d-%m-%Y","%Y/%m/%d"):
        try: return datetime.strptime(date_str, fmt).date()
        except: continue
    try: return datetime.fromisoformat(date_str).date()
    except: return None

def import_parsed_data(parsed, import_job, preview=False):
    start_time=time.time()
    family=ensure_exam_family()
    total=0; imported=0; skipped=0; duplicates=0; invalid=0; warnings_count=0; errors_count=0
    seen_hashes={}
    existing_hashes=set(Question.objects.values_list("source_hash", flat=True))
    report={"exam_sessions":[],"written_sessions":[],"details":[]}
    # Preload subjects cache with existing
    for subj in Subject.objects.all():
        _subject_cache[subj.code]=subj
        _subject_cache[subj.name]=subj
    for es in parsed["exam_sessions"]:
        total+=len(es.questions)
        exam_date_obj=parse_date(es.exam_date)
        status_map={"ACTIVE":"ACTIVE","CANCELLED":"CANCELLED","DEMO":"DEMO","ARCHIVED":"ARCHIVED"}
        status=status_map.get(es.status,"ACTIVE")
        if preview:
            report["exam_sessions"].append({"name":es.name,"route_id":es.route_id,"exam_type":es.exam_type,"specialization":es.specialization,"exam_date":str(exam_date_obj) if exam_date_obj else es.exam_date,"marks":es.marks,"declared":es.question_count_declared,"parsed":len(es.questions),"status":status,"is_demo":es.is_demo})
            for q in es.questions:
                h=hashlib.sha256(re.sub(r'\s+',' ', q.question_text.strip().lower()).encode('utf-8')).hexdigest() if q.question_text else ""
                if h and h in seen_hashes: duplicates+=1
                elif h: seen_hashes[h]=q
                if h and h in existing_hashes: duplicates+=1
                if not q.question_text or len(q.choices)<2: invalid+=1
                if not q.normalized_answer: warnings_count+=1
            continue
        slug_base=slugify(f"{es.name} {es.exam_type} {es.route_id}")[:180]
        try:
            exam_session=ExamSession.objects.get(route_id=es.route_id)
            exam_session.name=es.name; exam_session.exam_family=family; exam_session.exam_type=es.exam_type; exam_session.specialization=es.specialization; exam_session.exam_date=exam_date_obj; exam_session.marks=es.marks or exam_session.marks; exam_session.question_count=es.question_count_declared or len(es.questions); exam_session.status=status; exam_session.source_preview_url=es.preview_url; exam_session.source_exam_url=es.exam_url; exam_session.is_demo=es.is_demo; exam_session.save()
        except ExamSession.DoesNotExist:
            slug=slug_base; counter=1
            while ExamSession.objects.filter(slug=slug).exists():
                slug=f"{slug_base}-{counter}"; counter+=1
            exam_session=ExamSession.objects.create(exam_family=family,name=es.name,slug=slug,route_id=es.route_id,exam_type=es.exam_type,specialization=es.specialization,exam_date=exam_date_obj,marks=es.marks or 0,question_count=es.question_count_declared or len(es.questions),status=status,source_preview_url=es.preview_url,source_exam_url=es.exam_url,is_demo=es.is_demo)
        # Use transaction per exam for speed
        with transaction.atomic():
            # Batch warnings/duplicate inserts to reduce commits? For now handle per question but within transaction it's fast
            for q in es.questions:
                try:
                    if not q.question_text or not q.question_text.strip():
                        invalid+=1; warnings_count+=1
                        # Create warning only for missing text (important), not for every missing explanation
                        QuestionImportWarning.objects.create(import_job=import_job,question_number=q.question_number,exam_route_id=es.route_id,message="Missing question text - placeholder",raw_data=q.raw_markdown[:3000])
                        if not q.question_text:
                            q.question_text=f"[Question {q.question_number} - content not parsed]"
                    if len(q.choices)<4:
                        # Only warn if less than 4, but don't create DB row for each missing explanation case
                        if len(q.choices)<2:
                            QuestionImportWarning.objects.create(import_job=import_job,question_number=q.question_number,exam_route_id=es.route_id,message=f"Question has {len(q.choices)} choices",raw_data=q.raw_markdown[:3000])
                        warnings_count+=1
                    h=hashlib.sha256(re.sub(r'\s+',' ', q.question_text.strip().lower()).encode('utf-8')).hexdigest()
                    existing_q=Question.objects.filter(exam_session=exam_session, question_number=q.question_number).first()
                    if existing_q:
                        if existing_q.source_hash==h and existing_q.question_text==q.question_text:
                            skipped+=1; continue
                    is_global_duplicate=h in existing_hashes
                    if is_global_duplicate:
                        dup_q=Question.objects.filter(source_hash=h).first()
                        QuestionImportDuplicate.objects.create(import_job=import_job,question_text=q.question_text[:2000],source_hash=h,existing_question_id=dup_q.id if dup_q else None,similarity=1.0,raw_data=q.raw_markdown[:3000])
                        duplicates+=1
                    subject=ensure_subject_cached(q.category)
                    if not q.normalized_answer:
                        # Only create warning for blank, not for missing explanation
                        if warnings_count<2000: # limit to avoid too many
                            QuestionImportWarning.objects.create(import_job=import_job,question_number=q.question_number,exam_route_id=es.route_id,message="Blank/missing answer - marked unresolved",raw_data=q.raw_markdown[:2000])
                        warnings_count+=1
                        # For missing explanation, just count, don't DB insert (too many)
                    elif not q.has_explanation:
                        warnings_count+=1
                    if existing_q:
                        existing_q.subject=subject; existing_q.question_text=q.question_text; existing_q.explanation=q.explanation; existing_q.source_answer=q.source_answer; existing_q.normalized_answer=q.normalized_answer; existing_q.has_explanation=q.has_explanation; existing_q.is_resolved=bool(q.normalized_answer); existing_q.original_source_text=q.raw_markdown; existing_q.save()
                        existing_q.choices.all().delete()
                        question_obj=existing_q
                    else:
                        question_obj=Question.objects.create(exam_session=exam_session,subject=subject,question_number=q.question_number,question_text=q.question_text,explanation=q.explanation,source_answer=q.source_answer,normalized_answer=q.normalized_answer,has_explanation=q.has_explanation,is_resolved=bool(q.normalized_answer),source_hash=h,original_source_text=q.raw_markdown)
                        existing_hashes.add(h); imported+=1
                    # Bulk choices using bulk_create for speed
                    choice_objs=[]
                    for idx, choice in enumerate(q.choices):
                        label=choice.label.upper()
                        if label not in ("A","B","C","D"): continue
                        is_correct=(q.normalized_answer==label) if q.normalized_answer else False
                        choice_objs.append(Choice(question=question_obj,label=label,text=choice.text,is_correct=is_correct,display_order=idx))
                    if choice_objs:
                        Choice.objects.bulk_create(choice_objs)
                    if h not in seen_hashes:
                        seen_hashes[h]=q
                except Exception as exc:
                    import traceback; traceback.print_exc()
                    QuestionImportError.objects.create(import_job=import_job,question_number=q.question_number,exam_route_id=es.route_id,message=f"Import error Q{q.question_number}: {exc}",raw_data=q.raw_markdown[:3000]+f"\n---\n{exc}")
                    errors_count+=1; invalid+=1; skipped+=1; continue
        actual_count=exam_session.questions.count()
        if actual_count!=exam_session.question_count:
            exam_session.question_count=actual_count; exam_session.save(update_fields=["question_count"])
        report["exam_sessions"].append({"name":es.name,"route_id":es.route_id,"imported":actual_count})
    # Written
    for ws in parsed["written_sessions"]:
        total+=len(ws.written_questions)
        if preview:
            report["written_sessions"].append({"name":ws.name,"route_id":ws.route_id,"parsed":len(ws.written_questions),"declared":ws.question_count_declared})
            continue
        slug_base=slugify(ws.name)[:180]
        try:
            exam_session=ExamSession.objects.get(route_id=ws.route_id)
            exam_session.name=ws.name; exam_session.exam_family=family; exam_session.exam_type="Written"; exam_session.source_preview_url=ws.preview_url; exam_session.source_exam_url=ws.exam_url; exam_session.save()
        except ExamSession.DoesNotExist:
            slug=slug_base; counter=1
            while ExamSession.objects.filter(slug=slug).exists():
                slug=f"{slug_base}-{counter}"; counter+=1
            exam_session=ExamSession.objects.create(exam_family=family,name=ws.name,slug=slug,route_id=ws.route_id,exam_type="Written",specialization="",marks=0,question_count=ws.question_count_declared or len(ws.written_questions),status="ACTIVE",source_preview_url=ws.preview_url,source_exam_url=ws.exam_url,is_demo=False)
        with transaction.atomic():
            for wq in ws.written_questions:
                try:
                    if not wq.question_text:
                        invalid+=1; skipped+=1; continue
                    h=hashlib.sha256(re.sub(r'\s+',' ', wq.question_text.strip().lower()).encode('utf-8')).hexdigest()
                    existing_wq=WrittenQuestion.objects.filter(exam_session=exam_session, question_number=wq.question_number).first()
                    subject=ensure_subject_cached(wq.subject) if wq.subject else ensure_subject_cached("GENERAL")
                    marks_val=None
                    try:
                        if wq.marks and wq.marks.strip() not in ("???","???","?"):
                            m=re.search(r'\d+', wq.marks)
                            if m: marks_val=int(m.group())
                    except: marks_val=None
                    exam_date_obj=parse_date(wq.date)
                    if existing_wq:
                        if existing_wq.source_hash==h: skipped+=1; continue
                        existing_wq.subject=subject; existing_wq.question_text=wq.question_text; existing_wq.marks=marks_val; existing_wq.code=wq.code or ""; existing_wq.set_name=wq.set_name or ""; existing_wq.group=wq.group or ""; existing_wq.original_source_text=wq.raw_markdown; existing_wq.exam_date=exam_date_obj; existing_wq.save()
                    else:
                        WrittenQuestion.objects.create(exam_session=exam_session,subject=subject,question_number=wq.question_number,question_text=wq.question_text,marks=marks_val,code=wq.code or "",set_name=wq.set_name or "",group=wq.group or "",original_source_text=wq.raw_markdown,exam_date=exam_date_obj,source_hash=h)
                        imported+=1; existing_hashes.add(h)
                except Exception as exc:
                    QuestionImportError.objects.create(import_job=import_job,question_number=wq.question_number,exam_route_id=ws.route_id,message=f"Written error Q{wq.question_number}: {exc}",raw_data=wq.raw_markdown[:3000])
                    errors_count+=1; continue
        actual_w=exam_session.written_questions.count()
        exam_session.question_count=actual_w; exam_session.save(update_fields=["question_count"])
        report["written_sessions"].append({"name":ws.name,"imported":actual_w})
    processing_time=time.time()-start_time
    if not preview:
        import_job.total_records=total; import_job.imported=imported; import_job.skipped=skipped; import_job.duplicates=duplicates; import_job.invalid=invalid; import_job.warnings_count=warnings_count; import_job.errors_count=errors_count; import_job.processing_time_seconds=processing_time; import_job.report=report; import_job.status=QuestionImport.Status.COMPLETED; import_job.save()
    return {"total":total,"imported":imported,"skipped":skipped,"duplicates":duplicates,"invalid":invalid,"warnings":warnings_count,"errors":errors_count,"processing_time":processing_time,"report":report}
