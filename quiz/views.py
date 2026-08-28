
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from django.contrib import messages
import json, random
from exams.models import ExamSession
from questions.models import Question, Subject, Choice
from bookmarks.models import Bookmark
from .models import Quiz, QuizAttempt, UserAnswer, QuestionReview
from gamification.models import award_xp, XPTransaction
from accounts.models import DailyActivity

def _select_questions_for_attempt(user, mode, exam=None, subject=None, count=10, weak=False):
    # Smart selection: prioritize never attempted, recently incorrect, weak topics, not bookmarked etc.
    # IMPORTANT: When exam is specified, maintain exact serial order (question_number) as per uttoron.academy source.
    # Do NOT shuffle for exam-specific quizzes; preserve Q1..QN sequence.
    # For exam: include Blank/unresolved to keep 200 exact (Q21,129,172), for practice exclude unresolved.
    if exam:
        base = Question.objects.filter(active=True, exam_session=exam).order_by("question_number")
    else:
        base = Question.objects.filter(active=True, is_resolved=True)
    if subject:
        base = base.filter(subject=subject)
    if mode == "BOOKMARKED":
        bm_ids = Bookmark.objects.filter(user=user).values_list("question_id", flat=True) if user and user.is_authenticated else []
        base = base.filter(id__in=bm_ids)
        if not base.exists():
            # For bookmarked fallback, respect serial if exam given
            if exam:
                base = Question.objects.filter(active=True, exam_session=exam).order_by("question_number")[:count]
            else:
                base = Question.objects.filter(active=True, is_resolved=True).order_by("?")[:count]
            return list(base)
    if mode == "INCORRECT":
        incorrect_ids = UserAnswer.objects.filter(attempt__user=user, is_correct=False).values_list("question_id", flat=True)
        base = base.filter(id__in=incorrect_ids)
        if not base.exists():
            # fallback to ordered if exam else random
            if exam:
                base = Question.objects.filter(active=True, exam_session=exam).order_by("question_number")
            else:
                base = Question.objects.filter(active=True, is_resolved=True)
    if mode == "WEAK":
        # Detect weak subjects: lowest accuracy
        from analytics.models import UserSubjectPerformance
        # fallback: get subjects where user has low accuracy
        weak_subjects = UserAnswer.objects.filter(attempt__user=user).values("question__subject").annotate(acc=Avg("is_correct")).order_by("acc")[:3]
        if weak_subjects:
            s_ids = [w["question__subject"] for w in weak_subjects]
            base = base.filter(subject_id__in=s_ids)
    # Exam-specific: return exact serial slice (first `count` never_seen ordered by question_number)
    if exam and user and user.is_authenticated:
        seen_ids = QuestionReview.objects.filter(user=user).values_list("question_id", flat=True)
        never_seen = base.exclude(id__in=seen_ids).order_by("question_number")
        if never_seen.count() >= count:
            return list(never_seen[:count])
        # else fall through to serial-preserving pool below but still ordered
    # Prioritize never seen
    if user and user.is_authenticated:
        seen_ids = QuestionReview.objects.filter(user=user).values_list("question_id", flat=True)
        never_seen = base.exclude(id__in=seen_ids)
        # If exam provided, keep ordering deterministic
        if exam:
            never_seen = never_seen.order_by("question_number")
            base = base.order_by("question_number")
        if never_seen.count() >= count:
            # sample from never_seen efficiently - preserve serial if exam else random
            if exam:
                return list(never_seen[:count])
            ids = list(never_seen.values_list("id", flat=True)[:1000])
            sampled = random.sample(ids, min(count, len(ids)))
            # Preserve qids order as sampled, but fetch ordered by question_number if exam else as sampled
            qs = Question.objects.filter(id__in=sampled)
            if exam:
                qs = qs.order_by("question_number")
            # else maintain sampled order via mapping
            qmap = {q.id: q for q in qs}
            return [qmap[i] for i in sampled if i in qmap] if not exam else list(qs)
        # else combine never_seen + recently incorrect
        incorrect_ids = list(UserAnswer.objects.filter(attempt__user=user, is_correct=False).values_list("question_id", flat=True)[:500])
        # Build pool: never_seen + incorrect + random
        pool_ids = list(never_seen.values_list("id", flat=True)[:500]) + incorrect_ids
        # Fill to count with ordered if exam else random
        remaining = count - len(pool_ids)
        if remaining > 0:
            if exam:
                extra = list(base.exclude(id__in=pool_ids).order_by("question_number").values_list("id", flat=True)[:remaining])
                pool_ids += extra
            else:
                extra = list(base.exclude(id__in=pool_ids).values_list("id", flat=True)[:remaining*2])
                pool_ids += random.sample(extra, min(remaining, len(extra))) if extra else []
        # deduplicate and handle
        pool_ids = list(dict.fromkeys(pool_ids))  # preserve order, dedup
        if len(pool_ids) > count:
            if exam:
                # For exam, take first count by question_number order
                qs = Question.objects.filter(id__in=pool_ids).order_by("question_number")
                return list(qs[:count])
            pool_ids = random.sample(pool_ids, count)
        elif len(pool_ids) < count:
            # fill with ordered if exam
            if exam:
                extra = list(base.exclude(id__in=pool_ids).order_by("question_number").values_list("id", flat=True)[:count-len(pool_ids)])
            else:
                extra = list(base.exclude(id__in=pool_ids).values_list("id", flat=True)[:count-len(pool_ids)])
            pool_ids += extra
        if exam:
            return list(Question.objects.filter(id__in=pool_ids).order_by("question_number"))
        return list(Question.objects.filter(id__in=pool_ids))
    # anonymous: ordered if exam else random
    if exam:
        return list(base.order_by("question_number")[:count])
    ids = list(base.values_list("id", flat=True))
    if len(ids) > count:
        ids = random.sample(ids, count)
    return list(Question.objects.filter(id__in=ids))

def _get_exam(slug):
    try:
        return ExamSession.objects.get(slug=slug)
    except ExamSession.DoesNotExist:
        try:
            return ExamSession.objects.get(route_id=slug)
        except ExamSession.DoesNotExist:
            return get_object_or_404(ExamSession, Q(slug__iexact=slug) | Q(route_id__iexact=slug))

@login_required
def start_quiz(request, slug=None):
    mode = request.GET.get("mode","PRACTICE")
    count = int(request.GET.get("count",10))
    subject_slug = request.GET.get("subject")
    exam = None
    subject = None
    if slug:
        exam = _get_exam(slug)
    if subject_slug:
        subject = get_object_or_404(Subject, slug=subject_slug)
    # Validate count
    count = min(max(count,5), 200)
    # Select questions
    questions = _select_questions_for_attempt(request.user, mode, exam=exam, subject=subject, count=count, weak=(mode=="WEAK"))
    if not questions:
        messages.error(request, "No questions found for this selection.")
        return redirect("/exams/")
    # Create QuizAttempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        exam_session=exam,
        mode=mode,
        subject=subject,
        total_questions=len(questions),
        time_remaining_seconds= (len(questions)*60) if mode=="EXAM" else None,
        status="IN_PROGRESS"
    )
    # Prefetch: create UserAnswer placeholders? Or just rely on order list stored in session?
    # Store question order in session / via QuizAttempt relation: we will store via through? Simplest: store order as JSON in quiz field or use UserAnswer with is_skipped?
    # We'll store order via a simple JSON field: use attempt's quiz relation? For now store in DB via a many-to-many like order list encoded in time_remaining? Instead use cache/session.
    # Let's create a Quiz object to hold order, or store question ids in UserAnswer with null choice and is_skipped true? Better to store ids in session.
    request.session[f"attempt_{attempt.id}_qids"] = [q.id for q in questions]
    # Also create a Quiz for reference if needed
    return redirect("quiz_take", attempt_id=attempt.id)

@login_required
def quick_quiz(request):
    # 5/10/20 selection page or direct?
    count = int(request.GET.get("count",10))
    return start_quiz(request, slug=None)

@login_required
def weak_area_quiz(request):
    return start_quiz(request, slug=None, )

@login_required
def exam_mode_start(request, slug):
    exam = _get_exam(slug)
    # Exam simulation: all questions of that exam - include Blank/unresolved to keep 200 exact as Uttoron (Q21,129,172 Blank)
    questions = list(exam.questions.filter(active=True).order_by("question_number"))
    if not questions:
        messages.error(request, "No questions available for exam mode.")
        return redirect(exam.get_absolute_url() if hasattr(exam, "get_absolute_url") else f"/exams/{exam.slug}/")
    attempt = QuizAttempt.objects.create(
        user=request.user,
        exam_session=exam,
        mode="EXAM",
        total_questions=len(questions),
        time_remaining_seconds=len(questions)*60, # 1 min per question
        status="IN_PROGRESS"
    )
    request.session[f"attempt_{attempt.id}_qids"] = [q.id for q in questions]
    return redirect("quiz_take", attempt_id=attempt.id)

def get_attempt_questions(attempt, request):
    qids = request.session.get(f"attempt_{attempt.id}_qids")
    if not qids:
        # fallback: try to load from UserAnswers or recreate
        existing = list(attempt.answers.values_list("question_id", flat=True))
        if existing:
            qids = existing
        else:
            # recreate from exam or random
            if attempt.exam_session:
                qids = list(attempt.exam_session.questions.filter(active=True).values_list("id", flat=True)[:attempt.total_questions])
            else:
                qids = list(Question.objects.filter(active=True).values_list("id", flat=True)[:attempt.total_questions])
            request.session[f"attempt_{attempt.id}_qids"] = qids
    # Preserve order
    qs = Question.objects.filter(id__in=qids).select_related("subject","exam_session").prefetch_related("choices")
    # order by qids order
    qmap = {q.id: q for q in qs}
    ordered = [qmap[qid] for qid in qids if qid in qmap]
    return ordered

@login_required
def quiz_take(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    if attempt.status == "COMPLETED":
        return redirect("quiz_result", attempt_id=attempt.id)
    questions = get_attempt_questions(attempt, request)
    # Current index from attempt.current_question_index or query param
    idx = int(request.GET.get("q", attempt.current_question_index))
    idx = max(0, min(idx, len(questions)-1))
    # Handle mark for review etc.
    # Load existing answers
    answers = {a.question_id: a for a in attempt.answers.select_related("selected_choice")}
    # Update current index if not POST
    if request.method == "GET" and idx != attempt.current_question_index:
        attempt.current_question_index = idx
        attempt.save(update_fields=["current_question_index"])
    current_question = questions[idx] if questions else None
    # Navigator states
    nav_states = []
    for i, q in enumerate(questions):
        ans = answers.get(q.id)
        state = "unanswered"
        if ans:
            if ans.is_skipped or not ans.selected_label:
                state = "unanswered"
            else:
                state = "answered"
                if ans.marked_for_review:
                    state = "answered_marked"
            if ans.marked_for_review and state=="unanswered":
                state = "marked"
        if i == idx:
            state += " current"
        nav_states.append((i,q,state,ans))
    # Progress
    answered_count = sum(1 for a in answers.values() if a.selected_label)
    progress = int((answered_count / len(questions))*100) if questions else 0
    # For new QuestionNavigator component (spec: totalQuestions, currentQuestion, answeredQuestions, flaggedQuestions)
    # Use position (1..N) for navigator buttons – for exam N=200, position == question_number (1..200 inc. Blank Q21,129,172)
    answered_numbers = [i+1 for i, q in enumerate(questions) if answers.get(q.id) and answers[q.id].selected_label]
    flagged_numbers = [i+1 for i, q in enumerate(questions) if answers.get(q.id) and answers[q.id].marked_for_review]
    skipped_numbers = [i+1 for i, q in enumerate(questions) if answers.get(q.id) and answers[q.id].is_skipped]
    return render(request, "quiz/take.html", {
        "attempt": attempt,
        "questions": questions,
        "current": current_question,
        "idx": idx,
        "total": len(questions),
        "answers": answers,
        "nav_states": nav_states,
        "progress": progress,
        "answered_count": answered_count,
        "answered_numbers": answered_numbers,
        "flagged_numbers": flagged_numbers,
        "skipped_numbers": skipped_numbers,
    })

@login_required
@require_POST
def quiz_answer(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    if attempt.status != "IN_PROGRESS":
        return JsonResponse({"error":"Attempt not in progress"}, status=400)
    try:
        data = json.loads(request.body)
    except:
        data = request.POST
    question_id = data.get("question_id")
    choice_label = data.get("choice") or data.get("selected_label")
    marked = data.get("marked_for_review") == "true" or data.get("marked_for_review") is True
    time_taken = int(data.get("time_taken",0))
    question = get_object_or_404(Question, id=question_id)
    # Validate question belongs to attempt's question list
    qids = request.session.get(f"attempt_{attempt.id}_qids", [])
    if qids and int(question_id) not in qids:
        return JsonResponse({"error":"Question not in attempt"}, status=400)
    # Upsert UserAnswer
    selected_choice = None
    if choice_label:
        choice_label = choice_label.upper().strip()
        selected_choice = Choice.objects.filter(question=question, label=choice_label).first()
    # Determine is_correct
    is_correct = False
    is_skipped = not bool(choice_label)
    if choice_label and question.normalized_answer:
        is_correct = (choice_label == question.normalized_answer)
    ans, created = UserAnswer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            "selected_choice": selected_choice,
            "selected_label": choice_label or "",
            "is_correct": is_correct,
            "is_skipped": is_skipped,
            "time_taken_seconds": time_taken,
            "marked_for_review": marked,
        }
    )
    # Update QuestionReview for spaced repetition
    review, _ = QuestionReview.objects.get_or_create(user=request.user, question=question)
    review.total_attempts += 1
    if is_correct:
        review.correct_streak += 1
        review.incorrect_count = max(0, review.incorrect_count-1)
    else:
        if not is_skipped:
            review.incorrect_count += 1
            review.correct_streak = 0
    # simple next review: if correct streak >=3, delay 7 days else 1 day
    from datetime import timedelta
    if review.correct_streak >= 3:
        review.next_review_at = timezone.now() + timedelta(days=7)
    elif review.correct_streak >= 1:
        review.next_review_at = timezone.now() + timedelta(days=3)
    else:
        review.next_review_at = timezone.now() + timedelta(days=1)
    review.confidence = min(1.0, review.correct_streak / 5.0)
    review.save()
    # Return feedback for practice mode (immediate)
    return JsonResponse({
        "success": True,
        "is_correct": is_correct,
        "correct_answer": question.normalized_answer,
        "explanation": question.explanation if attempt.mode=="PRACTICE" else "",
        "xp_preview": 10 if is_correct else 0,
    })

@login_required
def quiz_submit(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    if attempt.status == "COMPLETED":
        return redirect("quiz_result", attempt_id=attempt.id)
    questions = get_attempt_questions(attempt, request)
    answers = {a.question_id: a for a in attempt.answers.all()}
    correct = sum(1 for a in answers.values() if a.is_correct)
    incorrect = sum(1 for a in answers.values() if not a.is_correct and not a.is_skipped and a.selected_label)
    skipped = len(questions) - len([a for a in answers.values() if a.selected_label])
    # Some questions may have no answer row yet -> count as skipped
    # Ensure total matches
    total = len(questions)
    score = round((correct/total)*100,2) if total else 0
    # time taken
    time_taken = int((timezone.now() - attempt.started_at).total_seconds())
    attempt.correct_count = correct
    attempt.incorrect_count = incorrect
    attempt.skipped_count = skipped
    attempt.score = score
    attempt.time_taken_seconds = time_taken
    attempt.status = "COMPLETED"
    attempt.completed_at = timezone.now()
    attempt.save()
    # XP awarding
    xp_earned = 0
    # Correct answer XP (10 per correct, but anti-abuse: only once per question per day? For now simple)
    xp_earned += correct * 10
    # Quiz completed bonus
    xp_earned += 25
    if score == 100:
        xp_earned += 50
    if attempt.mode == "EXAM":
        xp_earned += 100
    elif attempt.mode == "DAILY":
        xp_earned += 50
    attempt.xp_earned = xp_earned
    attempt.save(update_fields=["xp_earned"])
    # Award via gamification
    if xp_earned>0:
        award_xp(request.user, xp_earned, "QUIZ_COMPLETED" if attempt.mode!="EXAM" else "EXAM_COMPLETED", reference_type="QuizAttempt", reference_id=attempt.id, description=f"{attempt.mode} {correct}/{total}")
        # also award per correct? Already included in xp_earned, but we count as one transaction
    # Daily activity & streak
    from accounts.models import DailyActivity, Profile
    today = timezone.localdate()
    activity, created = DailyActivity.objects.get_or_create(user=request.user, date=today, defaults={"questions_answered":0,"xp_earned":0})
    activity.questions_answered += total
    activity.xp_earned += xp_earned
    activity.save()
    profile,_ = Profile.objects.get_or_create(user=request.user)
    profile.update_streak(today)
    # Check achievements
    try:
        from gamification.views import check_achievements
        check_achievements(request.user)
    except Exception as e:
        import traceback; traceback.print_exc()
    # Update subject performance
    try:
        from analytics.models import UserSubjectPerformance
        # Recalculate for subjects in this attempt
        from django.db.models import Avg, Count
        # For each subject, update
        subject_ids = set(q.subject_id for q in questions if q.subject_id)
        for sid in subject_ids:
            qs = UserAnswer.objects.filter(attempt__user=request.user, question__subject_id=sid)
            total_s = qs.count()
            corr = qs.filter(is_correct=True).count()
            acc = (corr/total_s*100) if total_s else 0
            perf, _ = UserSubjectPerformance.objects.get_or_create(user=request.user, subject_id=sid)
            perf.attempted = total_s
            perf.correct = corr
            perf.incorrect = total_s - corr
            perf.accuracy = round(acc,2)
            perf.save()
    except: pass
    messages.success(request, f"Quiz completed! Score {score}% +{xp_earned} XP")
    return redirect("quiz_result", attempt_id=attempt.id)

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt.objects.select_related("exam_session","subject"), id=attempt_id, user=request.user)
    if attempt.status != "COMPLETED":
        return redirect("quiz_take", attempt_id=attempt.id)
    questions = get_attempt_questions(attempt, request)
    answers = {a.question_id: a for a in attempt.answers.select_related("question","selected_choice")}
    # Build review list
    review_items = []
    for q in questions:
        ans = answers.get(q.id)
        review_items.append((q, ans))
    # Previous attempts comparison
    prev = QuizAttempt.objects.filter(user=request.user, exam_session=attempt.exam_session, status="COMPLETED").exclude(id=attempt.id).order_by("-score").first()
    # Weak/strong subject
    from django.db.models import Avg
    # For display, find subject performances
    return render(request, "quiz/result.html", {"attempt": attempt, "review_items": review_items, "prev": prev})

@login_required
def quiz_history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).select_related("exam_session").order_by("-started_at")
    paginator = Paginator(attempts, 20)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "quiz/history.html", {"attempts": page})
