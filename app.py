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
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from course_data import get_language_options, get_lesson, get_lessons, normalize_base_language, normalize_target_language


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data")).expanduser()
UPLOAD_DIR = DATA_DIR / "uploads"
SUBMISSIONS_FILE = DATA_DIR / "submissions.json"
USERS_FILE = DATA_DIR / "users.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
USER_SESSION_COOKIE = "code_tutor_session"
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


def openai_feedback_enabled() -> bool:
    return bool(os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip())


def configured_admin_names() -> set[str]:
    raw = os.getenv("ADMIN_USERS", "Elven,Elven.")
    return {normalize_name(name).casefold() for name in raw.split(",") if normalize_name(name)}


def is_admin_user(user: dict | None) -> bool:
    if not user:
        return False
    if user.get("isAdmin") is True or str(user.get("role", "")).lower() == "admin":
        return True
    normalized_name = normalize_name(user.get("name", "")).casefold()
    return normalized_name in configured_admin_names() or normalized_name.rstrip(".") in configured_admin_names()


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


def default_profile() -> dict:
    return {
        "knownLanguages": [],
        "baseLanguage": "",
        "languageExperienceChosen": False,
        "targetLanguage": "racket",
        "activeDay": 1,
        "checklists": {},
    }


def ensure_data_files() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if not SUBMISSIONS_FILE.exists():
        SUBMISSIONS_FILE.write_text("[]", encoding="utf-8")
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps({"users": [], "sessions": {}}, indent=2), encoding="utf-8")
    if not FEEDBACK_FILE.exists():
        FEEDBACK_FILE.write_text("[]", encoding="utf-8")


def read_submissions() -> list[dict]:
    ensure_data_files()
    return json.loads(SUBMISSIONS_FILE.read_text(encoding="utf-8"))


def write_submissions(submissions: list[dict]) -> None:
    ensure_data_files()
    SUBMISSIONS_FILE.write_text(json.dumps(submissions, indent=2, ensure_ascii=False), encoding="utf-8")


def read_feedback_records() -> list[dict]:
    ensure_data_files()
    return json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))


def write_feedback_records(records: list[dict]) -> None:
    ensure_data_files()
    FEEDBACK_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def read_user_store() -> dict:
    ensure_data_files()
    data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    if "users" not in data:
        data["users"] = []
    if "sessions" not in data:
        data["sessions"] = {}
    sync_admin_flags(data)
    return data


def write_user_store(data: dict) -> None:
    ensure_data_files()
    USERS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def public_user(user: dict) -> dict:
    return {"id": user["id"], "name": user["name"], "isAdmin": is_admin_user(user)}


def sync_admin_flags(data: dict) -> None:
    admin_names = configured_admin_names()
    for user in data.get("users", []):
        normalized_name = normalize_name(user.get("name", "")).casefold()
        if normalized_name in admin_names or normalized_name.rstrip(".") in admin_names:
            user["isAdmin"] = True
            user["role"] = "admin"


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip())


def find_user_by_name(users: list[dict], name: str) -> dict | None:
    normalized = normalize_name(name).casefold()
    return next((user for user in users if user.get("name", "").casefold() == normalized), None)


def current_user() -> dict | None:
    token = request.cookies.get(USER_SESSION_COOKIE, "")
    if not token:
        return None
    store = read_user_store()
    session = store.get("sessions", {}).get(token)
    if not session:
        return None
    return next((user for user in store["users"] if user["id"] == session.get("userId")), None)


def require_user(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "login required"}), 401
        return handler(*args, **kwargs)

    return wrapper


def require_admin(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "login required"}), 401
        if not is_admin_user(user):
            return jsonify({"error": "admin required"}), 403
        return handler(*args, **kwargs)

    return wrapper


def create_user_session_response(user: dict, store: dict):
    token = uuid.uuid4().hex
    store["sessions"][token] = {
        "userId": user["id"],
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    write_user_store(store)
    response = make_response(jsonify({"user": public_user(user), "profile": sanitize_profile(user.get("profile", {}))}))
    response.set_cookie(
        USER_SESSION_COOKIE,
        token,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        secure=request.is_secure,
        samesite="Lax",
    )
    return response


def sanitize_profile(profile: dict | None) -> dict:
    profile = profile or {}
    allowed_languages = {"cpp", "racket", "python", "java", "c"}
    known = [item for item in profile.get("knownLanguages", []) if item in allowed_languages]
    raw_base = str(profile.get("baseLanguage") or "").strip().lower()
    language_experience_chosen = bool(profile.get("languageExperienceChosen"))
    if "languageExperienceChosen" not in profile and (known or raw_base in allowed_languages):
        language_experience_chosen = True
    target = normalize_target_language(profile.get("targetLanguage", "racket"))
    try:
        active_day = int(profile.get("activeDay", 1))
    except (TypeError, ValueError):
        active_day = 1
    checklists = profile.get("checklists", {})
    if not isinstance(checklists, dict):
        checklists = {}
    base_language = normalize_base_language(raw_base) if raw_base in allowed_languages else (known[0] if known else "")
    if not language_experience_chosen:
        known = []
        base_language = ""
    return {
        "knownLanguages": list(dict.fromkeys(known[:1])),
        "baseLanguage": base_language,
        "languageExperienceChosen": language_experience_chosen,
        "targetLanguage": target,
        "activeDay": max(1, min(active_day, 56)),
        "checklists": checklists,
    }


def english_safe_submission(record: dict) -> dict:
    cleaned = dict(record)
    for field in ("title", "category", "studentNote", "contentPreview", "content", "feedback"):
        value = cleaned.get(field)
        if isinstance(value, str) and HAN_RE.search(value):
            if field == "feedback":
                cleaned[field] = (
                    "This is an older feedback record created before the English-only site update. "
                    "Submit the assignment again to receive English feedback."
                )
            elif field == "contentPreview":
                cleaned[field] = "Older submission preview hidden by the English-only site setting."
            elif field == "content":
                cleaned[field] = "Older submission content hidden by the English-only site setting."
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


def local_line_review(line: str, target_language: str) -> str:
    stripped = line.strip()
    if not stripped:
        return "Blank line used for readability."
    if target_language == "racket":
        if stripped.startswith("#lang"):
            return "Selects the Racket language for the file. This is normally the first line."
        if stripped.startswith(";"):
            return "Comment line. It explains code for a reader and does not run."
        if stripped.startswith("(define ("):
            return "Defines a function. The function name and parameters come after `define`."
        if stripped.startswith("(define "):
            return "Binds a name to a value. This is the normal Racket way to create a named value."
        if stripped.startswith("(display") or stripped.startswith("(printf"):
            return "Produces output. The function name comes first, followed by the value to print."
        if stripped.startswith("("):
            return "A function call or special form. Read the first item after `(` as the operation."
    if target_language == "python":
        if stripped.startswith("#"):
            return "Comment line. Python ignores it when running the program."
        if stripped.startswith("def "):
            return "Defines a function. The indented lines below belong to this function."
        if stripped.startswith(("if ", "elif ", "else")):
            return "Controls a branch. The colon starts an indented block."
        if stripped.startswith(("for ", "while ")):
            return "Starts a loop. The indented block repeats according to this line."
        if "print(" in stripped:
            return "Prints output to the console."
        if "=" in stripped:
            return "Creates or updates a name. Python does not require a declared type here."
    if target_language in {"c", "cpp", "java"}:
        if stripped.startswith(("//", "/*", "*")):
            return "Comment line. It documents the program and does not execute."
        if stripped.startswith("#include") or stripped.startswith("import "):
            return "Imports library support so the program can use external names."
        if "class " in stripped:
            return "Defines a class, grouping related data and behavior."
        if "main(" in stripped:
            return "Program entry point. Execution starts here for this sample."
        if stripped.startswith(("if ", "else if", "else")):
            return "Controls a branch. The block runs only for the matching condition."
        if stripped.startswith(("for ", "while ", "do ")):
            return "Starts a loop. The condition or counter controls repetition."
        if stripped.startswith("return"):
            return "Returns a value or exits the current function."
        if "printf" in stripped or "cout" in stripped or "System.out.println" in stripped:
            return "Prints output to the console."
        if stripped.endswith(";"):
            return "A statement. The semicolon marks the end of this instruction."
    return "A code line that should be checked against the lesson goal, surrounding block, and expected output."


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
    if target_language == "cpp" and "main(" not in code and lesson["day"] <= 12:
        notes.append("For early C++ foundation lessons, include a small `main` function so the program can run from the command line.")
    if target_language == "java" and "class " not in code and "record " not in code:
        notes.append("For Java, place the code inside a class or record so it matches normal Java structure.")
    if target_language not in {"c", "cpp"} and ("#include" in code or "std::" in code):
        notes.append("The submission still contains C++ syntax. Rewrite that part using the target language's normal idioms.")
    if len(lines) < 8:
        notes.append("This is a short submission, so the review focuses on every submitted line. Short code can still receive useful syntax and logic feedback.")
    if not notes:
        notes.append("The basic structure looks reasonable. Next, improve naming, test coverage, and edge-case handling.")

    line_reviews = [
        f"- L{index}: `{line.strip()}` - {local_line_review(line, target_language)}"
        for index, line in enumerate(code.splitlines(), start=1)
        if line.strip()
    ][:12]
    if not line_reviews:
        line_reviews = ["- No non-empty lines were available for line-by-line review."]

    return (
        "Local rule-based feedback:\n"
        f"- Lesson: {lesson['category']} - {lesson['title']}\n"
        f"- Target language: {target_language_name}\n"
        f"- Non-empty code lines detected: {len(lines)}\n"
        + "\n".join(f"- {note}" for note in notes)
        + "\n\nLine-by-line quick review:\n"
        + "\n".join(line_reviews)
        + "\n\nThis review used the built-in checker. Use the notes above to revise the program, then submit again for another pass."
    )


def build_feedback_prompt(lesson: dict, content: str, student_note: str) -> str:
    syntax_bridge = lesson.get("syntax_bridge", {})
    docs = syntax_bridge.get("docs", lesson.get("official_docs", []))
    doc_lines = "\n".join(f"- {doc['title']}: {doc['url']}" for doc in docs)
    target_language_name = lesson.get("target_language_name", "Racket")
    base_language_name = lesson.get("base_language_name", "C++")
    target_code = syntax_bridge.get("target") or syntax_bridge.get("racket", "")
    return f"""
You are a strict but friendly programming teacher. The student knows {base_language_name} and is following a 56-day course to learn {target_language_name}.

Today's lesson:
Day {lesson['day']}: {lesson['title']}
Category: {lesson['category']}
Goal: {lesson['goal']}
Known-language bridge: {lesson['cpp_bridge']}
Assignment: {lesson['assignment']}
Rubric: {'; '.join(lesson['grading_rubric'])}

Today's {base_language_name} to {target_language_name} syntax bridge:
Concept: {syntax_bridge.get('concept', 'None')}
Migration angle: {syntax_bridge.get('today_angle', 'None')}
{base_language_name} syntax:
```text
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
3. {target_language_name} style feedback, especially whether the code still follows {base_language_name} habits.
4. At least 5 concrete improvement points.
5. A recommended revised version or key revised snippet.
6. Which official documentation topic above the student should revisit.
7. Pick 3-6 important lines from the student's code and explain them line by line: what the line does, what syntax point it uses, and the closest {base_language_name} comparison. If the submission has fewer than 3 non-empty lines, analyze every non-empty line instead of dismissing the work as too short. Keep the sentences short, plain, and accurate.
8. A checklist the student must complete before tomorrow's lesson.
Important: short submissions still require concrete review. Explain what the existing lines do, what is correct, what is missing for a complete program, and how to improve them.
Do not invent runtime results you did not observe. If tests need to be run, explain exactly how the student should run them.
"""


def gemini_feedback(prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "").strip())
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text or "Gemini returned an empty response. Try submitting again."


def openai_feedback(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "").strip())
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text


def ai_feedback(lesson: dict, content: str, student_note: str) -> str:
    prompt = build_feedback_prompt(lesson, content, student_note)
    if os.getenv("GEMINI_API_KEY", "").strip():
        try:
            return gemini_feedback(prompt)
        except Exception as error:
            return local_feedback(lesson, content) + f"\n\nGemini AI grading failed: {error}"
    if os.getenv("OPENAI_API_KEY", "").strip():
        try:
            return openai_feedback(prompt)
        except Exception as error:
            return local_feedback(lesson, content) + f"\n\nOpenAI grading failed: {error}"
    return local_feedback(lesson, content)


@app.get("/")
def index():
    if not has_access():
        return send_from_directory(app.static_folder, "login.html")
    response = make_response(send_from_directory(app.static_folder, "index.html"))
    access_code = configured_access_code()
    if access_code and request.args.get("access", "") == access_code:
        response.set_cookie(
            "racket_tutor_access",
            access_code,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            secure=request.is_secure,
            samesite="Lax",
        )
    return response


@app.get("/feedback-admin")
def feedback_admin_page():
    if not has_access():
        return send_from_directory(app.static_folder, "login.html")
    response = make_response(send_from_directory(app.static_folder, "feedback-admin.html"))
    access_code = configured_access_code()
    if access_code and request.args.get("access", "") == access_code:
        response.set_cookie(
            "racket_tutor_access",
            access_code,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            secure=request.is_secure,
            samesite="Lax",
        )
    return response


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
    token = request.cookies.get(USER_SESSION_COOKIE, "")
    if token:
        store = read_user_store()
        store.get("sessions", {}).pop(token, None)
        write_user_store(store)
    response = make_response(jsonify({"ok": True}))
    response.delete_cookie(USER_SESSION_COOKIE)
    return response


@app.get("/api/me")
@require_access
def me():
    user = current_user()
    if not user:
        return jsonify({"user": None, "profile": None, "openaiFeedbackEnabled": openai_feedback_enabled()})
    return jsonify({
        "user": public_user(user),
        "profile": sanitize_profile(user.get("profile", {})),
        "openaiFeedbackEnabled": openai_feedback_enabled(),
    })


@app.post("/api/register")
@require_access
def register():
    payload = request.get_json(silent=True) or {}
    name = normalize_name(payload.get("name", ""))
    password = str(payload.get("password", ""))
    if len(name) < 2:
        return jsonify({"error": "name must be at least 2 characters"}), 400
    if len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400

    store = read_user_store()
    if find_user_by_name(store["users"], name):
        return jsonify({"error": "that name is already registered"}), 409

    user = {
        "id": uuid.uuid4().hex,
        "name": name,
        "passwordHash": generate_password_hash(password),
        "profile": sanitize_profile(payload.get("profile") or default_profile()),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    store["users"].append(user)
    return create_user_session_response(user, store)


@app.post("/api/login")
@require_access
def login():
    payload = request.get_json(silent=True) or {}
    name = normalize_name(payload.get("name", ""))
    password = str(payload.get("password", ""))
    store = read_user_store()
    user = find_user_by_name(store["users"], name)
    if not user or not check_password_hash(user.get("passwordHash", ""), password):
        return jsonify({"error": "invalid name or password"}), 401
    user["profile"] = sanitize_profile(user.get("profile", {}))
    return create_user_session_response(user, store)


@app.post("/api/profile")
@require_access
@require_user
def save_profile():
    payload = request.get_json(silent=True) or {}
    user = current_user()
    store = read_user_store()
    for stored_user in store["users"]:
        if stored_user["id"] == user["id"]:
            stored_user["profile"] = sanitize_profile(payload)
            write_user_store(store)
            return jsonify({"profile": stored_user["profile"]})
    return jsonify({"error": "user not found"}), 404


@app.get("/api/course")
@require_access
def course():
    target = normalize_target_language(request.args.get("target"))
    base = normalize_base_language(request.args.get("base"))
    return jsonify({"languages": get_language_options(), "target": target, "base": base, "lessons": get_lessons(target, base)})


@app.get("/api/course/<int:day>")
@require_access
def lesson(day: int):
    target = normalize_target_language(request.args.get("target"))
    base = normalize_base_language(request.args.get("base"))
    item = get_lesson(day, target, base)
    if not item:
        return jsonify({"error": "lesson not found"}), 404
    return jsonify(item)


@app.get("/api/submissions")
@require_access
def submissions():
    user = current_user()
    records = read_submissions()
    if user:
        records = [record for record in records if record.get("userId") == user["id"]]
    return jsonify({"submissions": [english_safe_submission(item) for item in reversed(records)]})


@app.post("/api/feedback")
@require_access
def create_feedback():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    category = str(payload.get("category", "bug")).strip().lower()
    page = str(payload.get("page", "")).strip()
    lesson_day = payload.get("day")
    target = normalize_target_language(payload.get("target", "racket"))

    if category not in {"bug", "content", "feature", "other"}:
        category = "other"
    if len(message) < 10:
        return jsonify({"error": "feedback must be at least 10 characters"}), 400
    if len(message) > 4000:
        return jsonify({"error": "feedback must be 4000 characters or fewer"}), 400

    user = current_user()
    try:
        lesson_day = int(lesson_day) if lesson_day else None
    except (TypeError, ValueError):
        lesson_day = None

    record = {
        "id": uuid.uuid4().hex,
        "category": category,
        "message": message,
        "page": page[:500],
        "day": lesson_day if lesson_day and 1 <= lesson_day <= 56 else None,
        "target": target,
        "status": "open",
        "adminNote": "",
        "userId": user["id"] if user else None,
        "userName": user["name"] if user else "Anonymous",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    records = read_feedback_records()
    records.append(record)
    write_feedback_records(records)
    return jsonify({"feedback": record}), 201


@app.get("/api/admin/feedback")
@require_access
@require_admin
def admin_feedback_records():
    records = read_feedback_records()
    status = str(request.args.get("status", "")).strip().lower()
    if status:
        records = [record for record in records if record.get("status") == status]
    return jsonify({"feedback": list(reversed(records))})


@app.patch("/api/admin/feedback/<feedback_id>")
@require_access
@require_admin
def update_feedback_record(feedback_id: str):
    payload = request.get_json(silent=True) or {}
    next_status = str(payload.get("status", "")).strip().lower()
    admin_note = str(payload.get("adminNote", "")).strip()
    if next_status and next_status not in {"open", "reviewing", "fixed", "closed"}:
        return jsonify({"error": "invalid feedback status"}), 400

    records = read_feedback_records()
    for record in records:
        if record.get("id") == feedback_id:
            if next_status:
                record["status"] = next_status
            if "adminNote" in payload:
                record["adminNote"] = admin_note[:2000]
            record["updatedAt"] = datetime.now(timezone.utc).isoformat()
            write_feedback_records(records)
            return jsonify({"feedback": record})
    return jsonify({"error": "feedback not found"}), 404


@app.post("/api/admin/users/sync")
@require_access
@require_admin
def admin_sync_user():
    payload = request.get_json(silent=True) or {}
    name = normalize_name(payload.get("name", ""))
    password = str(payload.get("password", ""))
    make_admin = bool(payload.get("isAdmin", True))

    if len(name) < 2:
        return jsonify({"error": "name must be at least 2 characters"}), 400
    if password and len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400

    store = read_user_store()
    user = find_user_by_name(store["users"], name)
    if not user:
        user = {
            "id": uuid.uuid4().hex,
            "name": name,
            "passwordHash": generate_password_hash(password or uuid.uuid4().hex),
            "profile": sanitize_profile(default_profile()),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        store["users"].append(user)
    elif password:
        user["passwordHash"] = generate_password_hash(password)

    if make_admin:
        user["isAdmin"] = True
        user["role"] = "admin"

    write_user_store(store)
    return jsonify({"user": public_user(user)})


@app.post("/api/submit")
@require_access
def submit_assignment():
    ensure_data_files()

    day = int(request.form.get("day", "1"))
    target = normalize_target_language(request.form.get("target", "racket"))
    base = normalize_base_language(request.form.get("base", "cpp"))
    lesson = get_lesson(day, target, base)
    if not lesson:
        return jsonify({"error": "invalid day"}), 400

    student_name = request.form.get("studentName", "").strip() or "Anonymous"
    user = current_user()
    if user and (not student_name or student_name == "Anonymous"):
        student_name = user["name"]
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
        "userId": user["id"] if user else None,
        "day": day,
        "target": target,
        "targetLanguage": lesson.get("target_language_name", "Racket"),
        "category": lesson["category"],
        "title": lesson["title"],
        "studentName": student_name,
        "studentNote": student_note,
        "filename": saved_filename,
        "contentPreview": content[:1000],
        "content": content,
        "feedback": feedback,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    records = read_submissions()
    records.append(record)
    write_submissions(records)

    return jsonify({"submission": record, "sampleCode": lesson["code"]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "5000")))
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    ensure_data_files()
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=args.debug)
