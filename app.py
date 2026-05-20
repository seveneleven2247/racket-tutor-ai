from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, request, send_from_directory
from werkzeug.utils import secure_filename

from course_data import get_language_options, get_lesson, get_lessons, normalize_target_language


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
SUBMISSIONS_FILE = DATA_DIR / "submissions.json"
ALLOWED_EXTENSIONS = {
    "rkt",
    "rktl",
    "txt",
    "md",
    "cpp",
    "cc",
    "cxx",
    "c",
    "h",
    "hpp",
    "py",
    "java",
    "json",
}

HAN_RE = re.compile(r"[\u3400-\u9fff]")

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__, static_folder="static", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-racket-tutor-secret")


def configured_access_code() -> str:
    return os.getenv("ACCESS_CODE", "").strip()


def has_access() -> bool:
    access_code = configured_access_code()
    if not access_code:
        return True
    submitted = (
        request.cookies.get("racket_tutor_access")
        or request.headers.get("X-Access-Code", "")
        or request.args.get("access", "")
    )
    return submitted == access_code


def require_access(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        if has_access():
            return handler(*args, **kwargs)
        return jsonify({"error": "access code required"}), 401

    return wrapper


def ensure_data_files() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if not SUBMISSIONS_FILE.exists():
        SUBMISSIONS_FILE.write_text("[]", encoding="utf-8")


def read_submissions() -> list[dict]:
    ensure_data_files()
    return json.loads(SUBMISSIONS_FILE.read_text(encoding="utf-8"))


def write_submissions(submissions: list[dict]) -> None:
    ensure_data_files()
    SUBMISSIONS_FILE.write_text(json.dumps(submissions, indent=2, ensure_ascii=False), encoding="utf-8")


def english_safe_submission(record: dict) -> dict:
    cleaned = dict(record)
    for field in ("title", "category", "studentNote", "contentPreview", "feedback"):
        value = cleaned.get(field)
        if isinstance(value, str) and HAN_RE.search(value):
            if field == "feedback":
                cleaned[field] = (
                    "This is an older feedback record created before the English-only site update. "
                    "Submit the assignment again to receive English feedback."
                )
            elif field == "contentPreview":
                cleaned[field] = "Older submission preview hidden by the English-only site setting."
            elif field == "studentNote":
                cleaned[field] = ""
            else:
                cleaned[field] = "Legacy submission"
    return cleaned


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def read_uploaded_text(path: Path) -> str:
    raw = path.read_bytes()
    return raw.decode("utf-8", errors="replace")


def local_feedback(lesson: dict, content: str) -> str:
    code = content.strip()
    lines = [line for line in code.splitlines() if line.strip()]
    notes: list[str] = []

    if not code:
        return "No assignment content was detected. Upload a file or paste code before requesting feedback."

    target_language = lesson.get("target_language", "racket")
    target_language_name = lesson.get("target_language_name", "Racket")
    if target_language == "racket" and "#lang racket" not in code and "#lang typed/racket" not in code:
        notes.append("For Racket, put `#lang racket` or `#lang typed/racket` on the first line.")
    if target_language == "racket" and "(define" not in code and lesson["day"] >= 4:
        notes.append("After Day 4, most Racket assignments should include at least one `define` for naming or abstraction practice.")
    if target_language == "racket" and "check-" not in code and lesson["day"] >= 19:
        notes.append("From Day 19 onward, add rackunit tests such as `check-equal?` when possible.")
    if target_language == "python" and "def " not in code and lesson["day"] >= 4:
        notes.append("For Python function days, include at least one `def` so the work practices function design.")
    if target_language == "c" and "#include" not in code:
        notes.append("For C, include the relevant headers, such as `#include <stdio.h>` for formatted output.")
    if target_language == "java" and "class " not in code and "record " not in code:
        notes.append("For Java, place the code inside a class or record so it matches normal Java structure.")
    if target_language != "c" and ("#include" in code or "std::" in code):
        notes.append("The submission still contains C++ syntax. Rewrite that part using the target language's normal idioms.")
    if len(lines) < 8:
        notes.append("The submission is short. Add more examples, tests, or concise explanation comments to show the concept clearly.")
    if not notes:
        notes.append("The basic structure looks reasonable. Next, improve naming, test coverage, and edge-case handling.")

    return (
        "Local rule-based feedback:\n"
        f"- Lesson: {lesson['category']} - {lesson['title']}\n"
        f"- Target language: {target_language_name}\n"
        f"- Non-empty code lines detected: {len(lines)}\n"
        + "\n".join(f"- {note}" for note in notes)
        + "\n\nSet OPENAI_API_KEY to receive deeper AI feedback with paragraph-level review and improvement suggestions."
    )


def ai_feedback(lesson: dict, content: str, student_note: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return local_feedback(lesson, content)

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    syntax_bridge = lesson.get("syntax_bridge", {})
    docs = syntax_bridge.get("docs", lesson.get("official_docs", []))
    doc_lines = "\n".join(f"- {doc['title']}: {doc['url']}" for doc in docs)
    target_language_name = lesson.get("target_language_name", "Racket")
    target_code = syntax_bridge.get("target") or syntax_bridge.get("racket", "")
    prompt = f"""
You are a strict but friendly programming teacher. The student knows C++ and is following a 56-day course to learn {target_language_name}.

Today's lesson:
Day {lesson['day']}: {lesson['title']}
Category: {lesson['category']}
Goal: {lesson['goal']}
C++ bridge: {lesson['cpp_bridge']}
Assignment: {lesson['assignment']}
Rubric: {'; '.join(lesson['grading_rubric'])}

Today's C++ to {target_language_name} syntax bridge:
Concept: {syntax_bridge.get('concept', 'None')}
Migration angle: {syntax_bridge.get('today_angle', 'None')}
C++ syntax:
```cpp
{syntax_bridge.get('cpp', '')}
```
{target_language_name} syntax:
```text
{target_code}
```
Translation steps: {'; '.join(syntax_bridge.get('translation_steps', []))}
Common pitfalls: {'; '.join(syntax_bridge.get('pitfalls', []))}
Official documentation:
{doc_lines}

Student note:
{student_note or 'None'}

Student submission:
```text
{content[:12000]}
```

Review in English. Use this exact structure:
1. Overall score out of 10.
2. Correctness feedback.
3. {target_language_name} style feedback, especially whether the code still follows C++ habits.
4. At least 5 concrete improvement points.
5. A recommended revised version or key revised snippet.
6. Which official documentation topic above the student should revisit.
7. Pick 3-6 important lines from the student's code and explain them line by line: what the line does, what syntax point it uses, and the closest C++ comparison. Keep the sentences short, plain, and accurate.
8. A checklist the student must complete before tomorrow's lesson.
Do not invent runtime results you did not observe. If tests need to be run, explain exactly how the student should run them.
"""
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text


@app.get("/")
def index():
    if not has_access():
        return send_from_directory(app.static_folder, "login.html")
    return send_from_directory(app.static_folder, "index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/access")
def access():
    access_code = configured_access_code()
    submitted = (request.get_json(silent=True) or {}).get("code", "").strip()
    if not access_code:
        return jsonify({"ok": True, "protected": False})
    if submitted != access_code:
        return jsonify({"error": "invalid access code"}), 401
    response = make_response(jsonify({"ok": True, "protected": True}))
    response.set_cookie(
        "racket_tutor_access",
        access_code,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        secure=request.is_secure,
        samesite="Lax",
    )
    return response


@app.post("/api/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("racket_tutor_access")
    return response


@app.get("/api/course")
@require_access
def course():
    target = normalize_target_language(request.args.get("target"))
    return jsonify({"languages": get_language_options(), "target": target, "lessons": get_lessons(target)})


@app.get("/api/course/<int:day>")
@require_access
def lesson(day: int):
    target = normalize_target_language(request.args.get("target"))
    item = get_lesson(day, target)
    if not item:
        return jsonify({"error": "lesson not found"}), 404
    return jsonify(item)


@app.get("/api/submissions")
@require_access
def submissions():
    return jsonify({"submissions": [english_safe_submission(item) for item in reversed(read_submissions())]})


@app.post("/api/submit")
@require_access
def submit_assignment():
    ensure_data_files()

    day = int(request.form.get("day", "1"))
    target = normalize_target_language(request.form.get("target", "racket"))
    lesson = get_lesson(day, target)
    if not lesson:
        return jsonify({"error": "invalid day"}), 400

    student_name = request.form.get("studentName", "").strip() or "Anonymous"
    student_note = request.form.get("studentNote", "").strip()
    pasted_code = request.form.get("code", "")
    file = request.files.get("file")

    saved_filename = None
    content = pasted_code

    if file and file.filename:
        if not allowed_file(file.filename):
            return jsonify({"error": "unsupported file type"}), 400
        original = secure_filename(file.filename)
        saved_filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}_{original}"
        path = UPLOAD_DIR / saved_filename
        file.save(path)
        content = read_uploaded_text(path)

    if not content.strip():
        return jsonify({"error": "empty submission"}), 400

    feedback = ai_feedback(lesson, content, student_note)
    record = {
        "id": uuid.uuid4().hex,
        "day": day,
        "target": target,
        "targetLanguage": lesson.get("target_language_name", "Racket"),
        "category": lesson["category"],
        "title": lesson["title"],
        "studentName": student_name,
        "studentNote": student_note,
        "filename": saved_filename,
        "contentPreview": content[:1000],
        "feedback": feedback,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    records = read_submissions()
    records.append(record)
    write_submissions(records)

    return jsonify({"submission": record})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "5000")))
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    ensure_data_files()
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=args.debug)
