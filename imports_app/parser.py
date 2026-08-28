"""
Robust Markdown parser for ExamPath Academy Question Bank
Handles both MCQ and Written sections with tolerance for formatting variations
"""
import re
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


@dataclass
class ParsedChoice:
    label: str  # A,B,C,D
    text: str
    is_correct_visual: bool = False  # if ✅ present


@dataclass
class ParsedQuestion:
    question_number: int
    category: str  # raw category like MENTAL-ABILITY, may be empty
    source_answer: str  # raw answer like 'b', 'Blank'
    normalized_answer: Optional[str]  # A,B,C,D or None
    question_text: str
    choices: List[ParsedChoice] = field(default_factory=list)
    explanation: str = ""
    raw_markdown: str = ""
    has_explanation: bool = False
    # For traceability
    exam_route_id: str = ""
    exam_name: str = ""


@dataclass
class ParsedWrittenQuestion:
    question_number: int
    subject: str
    marks: Optional[str]
    code: Optional[str]
    set_name: Optional[str]
    group: Optional[str]
    date: Optional[str]
    question_text: str
    raw_markdown: str = ""
    exam_slug: str = ""


@dataclass
class ParsedExamSession:
    name: str  # e.g., "50th BCS"
    route_id: str
    exam_type: str
    specialization: str
    exam_date: Optional[str]  # raw string
    marks: Optional[int]
    question_count_declared: int
    preview_url: str
    exam_url: str
    description: str = ""
    status: str = "ACTIVE"  # ACTIVE, CANCELLED, DEMO
    is_demo: bool = False
    questions: List[ParsedQuestion] = field(default_factory=list)
    written_questions: List[ParsedWrittenQuestion] = field(default_factory=list)
    raw_header: str = ""


def normalize_answer(raw: str) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip().strip('`').strip()
    if not raw or raw.lower() == 'blank':
        return None
    first = raw[0].upper()
    if first in ('A','B','C','D'):
        return first
    return None

def slugify_code(code: str) -> str:
    # normalize subject code: uppercase, hyphens
    if not code:
        return ""
    code = code.strip().upper()
    # keep as is but ensure hyphens
    code = re.sub(r'\s+', '-', code)
    code = re.sub(r'[^A-Z0-9\-\_]', '-', code)
    code = re.sub(r'-+', '-', code).strip('-')
    return code

def hash_question(text: str) -> str:
    norm = re.sub(r'\s+', ' ', text.strip().lower())
    # Also normalize unicode variations? keep simple
    return hashlib.sha256(norm.encode('utf-8')).hexdigest()


# Regex patterns
EXAM_HEADER_RE = re.compile(r'^###\s+(\d+)\.\s+(.+?)(?:\s*\((\d{4}-\d{2}-\d{2}|22021-\d{2}-\d{2})\))?\s*$', re.MULTILINE)
ROUTE_ID_RE = re.compile(r'Route ID.*?`([^`]+)`', re.DOTALL | re.IGNORECASE)
TYPE_DATE_MARKS_RE = re.compile(r'\*?\*?Type:\*?\*?\s*(.*?)\s*\|\s*\*?\*?Date:\*?\*?\s*(.*?)\s*\|\s*\*?\*?Marks:\*?\*?\s*Marks\s*(\d+)', re.IGNORECASE)
PREVIEW_RE = re.compile(r'Preview:\s*(https[^\s\)]+)', re.IGNORECASE)
EXAM_URL_RE = re.compile(r'Exam \(login\):\s*(https[^\s\)]+)', re.IGNORECASE)
QUESTIONS_COUNT_RE = re.compile(r'Questions:\s*\**\s*(\d+)', re.IGNORECASE)
# Also for written header: ### 1. 50th-bcs-written
WRITTEN_HEADER_RE = re.compile(r'^###\s+\d+\.\s+([a-zA-Z0-9\-]+)\s*$', re.MULTILINE)

# MCQ question block: #### Question 1 [CATEGORY] - Answer: `b`
MCQ_QUESTION_RE = re.compile(r'^####\s+Question\s+(\d+)\s*\[([^\]]*)\]\s*-\s*Answer:\s*`([^`]*?)`\s*$', re.MULTILINE)
# Alternative written question: #### Question:1 [Bangla 1st Paper] (Marks: ???, Code: ???, Set: ?????, Group: ..., Date: ...)
WRITTEN_QUESTION_RE = re.compile(r'^####\s+Question\s*:\s*(\d+)\s*\[([^\]]+)\]\s*\(([^\)]+)\)\s*$', re.MULTILINE)

# Choice line: - **A.** text optional ✅
CHOICE_RE = re.compile(r'^- \*\*([A-D])\.\*\*\s*(.*?)\s*(✅)?\s*$', re.MULTILINE)
# Details block
DETAILS_RE = re.compile(r'<details><summary>.*?Explanation.*?</summary>(.*?)</details>', re.DOTALL | re.IGNORECASE)

# For question text: **Q:** text
QUESTION_TEXT_RE = re.compile(r'^\*\*Q:\*\*\s*(.*?)\s*$', re.MULTILINE | re.DOTALL)


def parse_mcq_question_block(block: str, route_id: str = "", exam_name: str = "") -> Optional[ParsedQuestion]:
    """
    Parse a single MCQ block including question header, Q, choices, explanation
    block is the markdown segment starting at #### Question and ending before next #### or ### or ##
    """
    # Find header
    m = MCQ_QUESTION_RE.search(block)
    if not m:
        return None
    qnum = int(m.group(1))
    category = m.group(2).strip()
    source_answer = m.group(3).strip()
    normalized = normalize_answer(source_answer)

    # Question text: after header, find **Q:**
    q_text = ""
    q_text_match = QUESTION_TEXT_RE.search(block)
    if q_text_match:
        # Find first choice position after header
        m_choice = re.search(r'^- \*\*[A-D]\.\*\*', block, re.MULTILINE)
        choice_start = m_choice.start() if m_choice else -1
        if choice_start != -1 and choice_start > q_text_match.start():
            q_section = block[q_text_match.start():choice_start]
            q_text = re.sub(r'^\*\*Q:\*\*\s*', '', q_section.strip(), flags=re.MULTILINE)
            q_text = q_text.strip()
        else:
            q_text = q_text_match.group(1).strip()
        # If still empty, fallback to capturing lines between **Q:** and choice, handling multiline images etc.
        if not q_text:
            # Check if block contains an image or non-Q content before choices
            # Take substring between header end and choice start
            header_end = block.find("\n", block.find("#### Question"))
            if header_end != -1 and choice_start != -1:
                candidate = block[header_end:choice_start].strip()
                # Remove **Q:** lines that are empty and keep any remaining lines (e.g., image markdown, second line)
                # If candidate contains non-empty after removing **Q:**, use it
                cleaned = re.sub(r'\*\*Q:\*\*\s*', '', candidate).strip()
                # Remove empty lines and choice markers
                lines = [l.strip() for l in cleaned.splitlines() if l.strip() and not l.strip().startswith("- **")]
                if lines:
                    q_text = "\n".join(lines).strip()
                # If still empty, try to extract any markdown image or placeholder
                if not q_text:
                    # Look for image pattern ![...]
                    img_match = re.search(r'!\[.*?\]\(.*?\)', candidate)
                    if img_match:
                        q_text = img_match.group(0)
                    else:
                        # Keep candidate as raw if not empty but not just Q:
                        if candidate and candidate != "**Q:**":
                            q_text = candidate.replace("**Q:**","").strip()
    else:
        # fallback: try to extract content between header and first choice
        m_choice = re.search(r'^- \*\*[A-D]\.\*\*', block, re.MULTILINE)
        if m_choice:
            header_end = block.find("\n", block.find("#### Question"))
            candidate = block[header_end:m_choice.start()].strip()
            # Remove any empty **Q:** markers
            candidate = re.sub(r'\*\*Q:\*\*\s*', '', candidate).strip()
            q_text = candidate
        else:
            lines = block.splitlines()
            q_text = ""
            for line in lines[1:]:
                if line.strip().startswith("**Q:**"):
                    q_text = line.replace("**Q:**","").strip()
                    break

    # Choices
    choices = []
    for cm in CHOICE_RE.finditer(block):
        label = cm.group(1).strip()
        text = cm.group(2).strip()
        has_check = cm.group(3) is not None
        # Remove trailing ✅ if present in text?
        if text.endswith("✅"):
            text = text[:-1].strip()
            has_check = True
        choices.append(ParsedChoice(label=label, text=text, is_correct_visual=has_check))

    # If choices missing, try alternative pattern without **?
    if len(choices) < 2:
        # Try looser pattern: - **A.** or - A.
        alt_choice_re = re.compile(r'^-.*?([A-D])\.\s*(.*?)\s*(✅)?\s*$', re.MULTILINE)
        # But avoid false positives
        pass

    # Explanation
    expl_match = DETAILS_RE.search(block)
    if expl_match:
        explanation = expl_match.group(1).strip()
        has_expl = True
    else:
        # Look for collapsible without details? Or just after choices?
        explanation = ""
        has_expl = False
        # Also check for <details> without closing? Just grab remainder
        # We'll search for Explanation keyword
        if "Explanation" in block:
            # fallback: take after choices
            pass

    raw = block.strip()

    # If no is_correct from Answer, but visual check exists, we can infer? But spec says don't infer, keep source.
    # We'll keep normalized from source_answer, not from visual.

    return ParsedQuestion(
        question_number=qnum,
        category=category,
        source_answer=source_answer,
        normalized_answer=normalized,
        question_text=q_text,
        choices=choices,
        explanation=explanation,
        raw_markdown=raw,
        has_explanation=has_expl,
        exam_route_id=route_id,
        exam_name=exam_name,
    )


def parse_written_question_block(block: str, exam_slug: str = "") -> Optional[ParsedWrittenQuestion]:
    m = WRITTEN_QUESTION_RE.search(block)
    if not m:
        return None
    qnum = int(m.group(1))
    subject = m.group(2).strip()
    meta_str = m.group(3)
    # meta_str like: Marks: ???, Code: ???, Set: ?????, Group: Technical, Date: 2026-04-09
    meta = {}
    for part in meta_str.split(','):
        if ':' in part:
            k,v = part.split(':',1)
            meta[k.strip().lower()] = v.strip()

    # Question text: after header, there is "Question:\n..." until "---" or next header
    # Structure:
    # Question:
    # 1
    # ... actual content ...
    # ---
    # So extract between "Question:" and "\n---"
    q_text = ""
    # Find "Question:" marker
    q_start = block.find("Question:")
    if q_start != -1:
        after = block[q_start + len("Question:"):]
        # remove leading newline and number line? First line after is question number duplicate, then actual content
        # We'll take everything after first newline and number
        lines = after.strip().splitlines()
        # First line might be just number
        if lines and lines[0].strip().isdigit():
            lines = lines[1:]
        # Join until "---" line
        content_lines = []
        for line in lines:
            if line.strip() == "---":
                break
            content_lines.append(line)
        q_text = "\n".join(content_lines).strip()
    else:
        q_text = block.strip()

    return ParsedWrittenQuestion(
        question_number=qnum,
        subject=subject,
        marks=meta.get('marks'),
        code=meta.get('code'),
        set_name=meta.get('set'),
        group=meta.get('group'),
        date=meta.get('date'),
        question_text=q_text,
        raw_markdown=block.strip(),
        exam_slug=exam_slug,
    )


def parse_markdown_file(file_path: str) -> Dict:
    """
    Main parse function. Returns dict with:
    - exam_sessions: List[ParsedExamSession]
    - written_sessions: List[ParsedExamSession] (with written_questions)
    - stats: dict
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Split into preli and written sections
    written_split_marker = "## BCS Written"
    preli_text = text
    written_text = ""
    if written_split_marker in text:
        parts = text.split(written_split_marker, 1)
        preli_text = parts[0]
        written_text = written_split_marker + parts[1]

    exam_sessions: List[ParsedExamSession] = []
    # Find all exam headers in preli_text
    # Use regex to find positions
    exam_headers = list(EXAM_HEADER_RE.finditer(preli_text))
    # For robustness, also handle "### 1. 50th BCS - General (...)" etc. Already covered.
    # If no matches, fallback to searching for "###" lines
    if not exam_headers:
        fallback = re.finditer(r'^###\s+.+', preli_text, re.MULTILINE)
        exam_headers = list(fallback)

    # We'll iterate by slicing text between headers
    for idx, match in enumerate(exam_headers):
        header_line = match.group(0)
        # Extract name and date
        # match groups: 1=number, 2=name+type, 3=date
        try:
            exam_full = match.group(2).strip() if match.lastindex >=2 else header_line.replace('###','').strip()
        except:
            exam_full = header_line.strip()
        exam_date_raw = match.group(3) if match.lastindex >=3 and match.group(3) else ""
        # Determine start and end positions
        start = match.start()
        end = exam_headers[idx+1].start() if idx+1 < len(exam_headers) else len(preli_text)
        # But if written split exists, ensure end doesn't exceed preli boundary
        section_text = preli_text[start:end]
        # Now parse exam metadata from section_text
        # Header name parsing: e.g., "50th BCS - General" or "48th BCS - Special (Health) Medical Part"
        # We'll try to separate BCS name from type suffix
        # Example header_line: "### 1. 50th BCS - General (2026-01-30)"
        # Already extracted exam_full contains "50th BCS - General"
        # Use split on " - " to separate
        name_part = exam_full
        # Remove possible trailing date already removed; exam_full shouldn't have date due to regex
        # Now detect type: if " - " present, first part is BCS name, rest is type
        if " - " in name_part:
            parts_type = name_part.split(" - ", 1)
            bcs_name = parts_type[0].strip()
            type_part = parts_type[1].strip()
        else:
            bcs_name = name_part.strip()
            type_part = "General"

        # Route ID
        route_match = ROUTE_ID_RE.search(section_text)
        route_id = route_match.group(1).strip() if route_match else slugify_code(bcs_name + "-" + type_part)

        # Type/Date/Marks line: alternative parse
        type_line_match = TYPE_DATE_MARKS_RE.search(section_text)
        exam_type = type_part
        exam_date_str = exam_date_raw
        marks_val = 100
        if type_line_match:
            exam_type = type_line_match.group(1).strip() or type_part
            exam_date_str = type_line_match.group(2).strip() or exam_date_raw
            try:
                marks_val = int(type_line_match.group(3).strip())
            except:
                marks_val = 100
        else:
            # Fallback: search for Marks
            marks_fallback = re.search(r'Marks.*?(\d+)', section_text, re.IGNORECASE)
            if marks_fallback:
                try:
                    marks_val = int(marks_fallback.group(1))
                except:
                    pass
            date_fallback = re.search(r'Date:\s*\*+\s*([0-9\-\?]+)', section_text, re.IGNORECASE)
            if not date_fallback:
                date_fallback = re.search(r'Date:\s*([0-9\-\?]+)', section_text, re.IGNORECASE)
            if date_fallback and not exam_date_str:
                exam_date_str = date_fallback.group(1).strip()
            type_fallback = re.search(r'Type:\s*\*+\s*([^|\n]+)', section_text, re.IGNORECASE)
            if not type_fallback:
                type_fallback = re.search(r'Type:\s*([^|\n]+)', section_text, re.IGNORECASE)
            if type_fallback:
                # Clean stars
                raw_type = type_fallback.group(1).strip()
                raw_type = re.sub(r'^\*+', '', raw_type).strip()
                raw_type = re.sub(r'\*+$', '', raw_type).strip()
                # Remove trailing | etc
                raw_type = raw_type.split("|")[0].strip()
                exam_type = raw_type

        # Detect specialization from exam_type: e.g., "Special (Health) Medical Part" -> specialization Medical, Dental etc.
        specialization = ""
        # Common pattern: split exam_type by details
        # If contains "Medical", "Dental", "General", "Education"
        lower_type = exam_type.lower()
        if "medical" in lower_type:
            specialization = "Medical"
        elif "dental" in lower_type:
            specialization = "Dental"
        elif "education" in lower_type:
            specialization = "Education"
        elif "general part" in lower_type:
            # Keep type as is but specialization empty? Actually for health we have General Part vs Medical
            # We'll keep specialization for medical/dental else blank
            pass

        # Correct exam_type to normalized? Keep original but also store specialization
        # Ensure route_id case preserved but also store original

        # Preview and Exam URLs
        preview_match = PREVIEW_RE.search(section_text)
        preview_url = preview_match.group(1).strip() if preview_match else f"https://uttoron.academy/QuestionBank/QuestionPreview/{route_id}"
        exam_url_match = EXAM_URL_RE.search(section_text)
        exam_url = exam_url_match.group(1).strip() if exam_url_match else f"https://uttoron.academy/QuestionBank/Question/{route_id}"

        # Declared question count
        qcount_match = QUESTIONS_COUNT_RE.search(section_text)
        declared_qcount = int(qcount_match.group(1)) if qcount_match else 0

        # Status detection: check for Cancelled, Demo
        status = "ACTIVE"
        is_demo = False
        # Header may contain "Cancelled" or route D-M, or name Demo
        if "cancelled" in header_line.lower() or "cancelled" in exam_full.lower() or "cancelled" in section_text.lower()[:500]:
            status = "CANCELLED"
        elif "demo" in bcs_name.lower() or route_id == "D-M":
            status = "DEMO"
            is_demo = True
        elif "dental" in lower_type or "medical" in lower_type:
            status = "ACTIVE"  # Special health still active

        # Fix date anomaly 22021
        if exam_date_str and exam_date_str.startswith("22021"):
            exam_date_str = exam_date_str.replace("22021", "2021")

        # Now parse MCQ questions inside this section
        # Split by #### Question
        # Find all MCQ question headers positions
        mcq_headers = list(MCQ_QUESTION_RE.finditer(section_text))
        questions: List[ParsedQuestion] = []
        for q_idx, q_match in enumerate(mcq_headers):
            q_start = q_match.start()
            q_end = mcq_headers[q_idx+1].start() if q_idx+1 < len(mcq_headers) else len(section_text)
            # But need to stop before next exam header? Already limited to section_text
            # However, written section after? Not in preli_text, so okay
            q_block = section_text[q_start:q_end]
            # For last block, ensure not including following exam header? Actually section_text ends at next exam header, so safe
            parsed_q = parse_mcq_question_block(q_block, route_id=route_id, exam_name=bcs_name)
            if parsed_q:
                questions.append(parsed_q)
            else:
                # Try to create warning for malformed
                pass

        # Also handle edge where category empty [] - our regex handles empty inside [] via * but we used +? Actually we used [^\]]* should handle empty. Good.
        # For questions where answer blank etc, still parsed.

        # If no questions found via regex but section contains "#### Question", try looser
        if not questions:
            # attempt alternative pattern: #### Question 1 [] etc maybe missing dash? Let's search for any #### Question
            loose_headers = list(re.finditer(r'^####\s+Question\s+.*$', section_text, re.MULTILINE))
            if loose_headers and not mcq_headers:
                for qi, lh in enumerate(loose_headers):
                    start = lh.start()
                    end = loose_headers[qi+1].start() if qi+1 < len(loose_headers) else len(section_text)
                    block = section_text[start:end]
                    # Try to parse with fallback: extract question_number, category, answer manually
                    # Already try our parser
                    p = parse_mcq_question_block(block, route_id, bcs_name)
                    if p:
                        questions.append(p)

        exam_session = ParsedExamSession(
            name=bcs_name,
            route_id=route_id,
            exam_type=exam_type,
            specialization=specialization,
            exam_date=exam_date_str if exam_date_str and exam_date_str != "???" else None,
            marks=marks_val,
            question_count_declared=declared_qcount,
            preview_url=preview_url,
            exam_url=exam_url,
            status=status,
            is_demo=is_demo,
            questions=questions,
            raw_header=header_line,
        )
        exam_sessions.append(exam_session)

    # Parse Written sessions
    written_sessions: List[ParsedExamSession] = []
    if written_text:
        # Find written headers: "### 1. 50th-bcs-written"
        wh_headers = list(re.finditer(r'^###\s+\d+\.\s+([^\n]+)\s*$', written_text, re.MULTILINE))
        # Filter to only those that look like slugs (contain -written or bcs)
        # But all under written section are written, so accept all
        for idx, wh in enumerate(wh_headers):
            slug_line = wh.group(1).strip()
            # slug_line may be like "1. 50th-bcs-written" includes number already? Actually regex captures after number
            # So slug_line is "50th-bcs-written"
            slug = slug_line.strip()
            # Clean slug: remove possible markdown? Ensure
            start = wh.start()
            end = wh_headers[idx+1].start() if idx+1 < len(wh_headers) else len(written_text)
            section = written_text[start:end]

            # Extract preview/exam URLs if present
            preview_match = re.search(r'Preview:\s*(https[^\s\)]+)', section, re.IGNORECASE)
            preview_url = preview_match.group(1).strip() if preview_match else f"https://uttoron.academy/QuestionBank/WrittenQuestionPreview/{slug}"
            exam_url_match = re.search(r'Exam \(login\):\s*(https[^\s\)]+)', section, re.IGNORECASE)
            exam_url = exam_url_match.group(1).strip() if exam_url_match else f"https://uttoron.academy/QuestionBank/WrittenQuestion/{slug}"
            qcount_match = re.search(r'Questions:\s*(\d+)', section, re.IGNORECASE)
            declared = int(qcount_match.group(1)) if qcount_match else 0

            # Parse written questions in this section
            wq_headers = list(WRITTEN_QUESTION_RE.finditer(section))
            w_questions = []
            for qi, wmh in enumerate(wq_headers):
                w_start = wmh.start()
                w_end = wq_headers[qi+1].start() if qi+1 < len(wq_headers) else len(section)
                block = section[w_start:w_end]
                pw = parse_written_question_block(block, exam_slug=slug)
                if pw:
                    w_questions.append(pw)

            # If no written questions found but section contains Question: pattern, try loose
            # Create a ParsedExamSession representing written exam
            ws = ParsedExamSession(
                name=slug,
                route_id=slug,
                exam_type="Written",
                specialization="",
                exam_date=None,
                marks=None,
                question_count_declared=declared or len(w_questions),
                preview_url=preview_url,
                exam_url=exam_url,
                status="ACTIVE",
                is_demo=False,
                questions=[],
                written_questions=w_questions,
                raw_header=wh.group(0),
            )
            written_sessions.append(ws)

    stats = {
        "total_exam_sessions": len(exam_sessions),
        "total_written_sessions": len(written_sessions),
        "total_mcq_questions": sum(len(es.questions) for es in exam_sessions),
        "total_written_questions": sum(len(ws.written_questions) for ws in written_sessions),
    }

    return {
        "exam_sessions": exam_sessions,
        "written_sessions": written_sessions,
        "stats": stats,
        "raw_preli_text": preli_text[:5000],  # sample
    }


def validate_parsed_data(parsed: Dict) -> Dict[str, List[str]]:
    warnings = []
    errors = []
    for es in parsed["exam_sessions"]:
        if not es.route_id:
            errors.append(f"Exam {es.name} missing route_id")
        if len(es.questions) == 0:
            warnings.append(f"Exam {es.name} ({es.route_id}) has 0 questions parsed but declared {es.question_count_declared}")
        if len(es.questions) != es.question_count_declared and es.question_count_declared !=0:
            warnings.append(f"Exam {es.name} question count mismatch: declared {es.question_count_declared}, parsed {len(es.questions)}")
        for q in es.questions:
            if not q.question_text:
                errors.append(f"Exam {es.route_id} Q{q.question_number} missing question text")
            if len(q.choices) < 4:
                warnings.append(f"Exam {es.route_id} Q{q.question_number} has {len(q.choices)} choices (expected 4)")
            if not q.normalized_answer:
                warnings.append(f"Exam {es.route_id} Q{q.question_number} has blank/missing answer")
            if not q.has_explanation:
                warnings.append(f"Exam {es.route_id} Q{q.question_number} missing explanation")
    for ws in parsed["written_sessions"]:
        if len(ws.written_questions) == 0:
            warnings.append(f"Written {ws.name} has 0 questions")
    return {"warnings": warnings, "errors": errors}
