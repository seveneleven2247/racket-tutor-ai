from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
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
ONLINE_WINDOW_SECONDS = 15 * 60
SESSION_TOUCH_SECONDS = 30
JUDGE0_DEFAULT_URL = "https://ce.judge0.com"
JUDGE0_DEFAULT_LANGUAGE_IDS = {
    "c": 103,
    "cpp": 105,
    "java": 91,
    "python": 109,
}
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


def judge0_api_url() -> str:
    return os.getenv("JUDGE0_API_URL", JUDGE0_DEFAULT_URL).strip().rstrip("/")


def judge0_language_ids() -> dict[str, int]:
    language_ids = dict(JUDGE0_DEFAULT_LANGUAGE_IDS)
    raw = os.getenv("JUDGE0_LANGUAGE_IDS", "").strip()
    if raw:
        try:
            overrides = json.loads(raw)
            for language, language_id in overrides.items():
                language_ids[normalize_target_language(language)] = int(language_id)
        except (TypeError, ValueError, json.JSONDecodeError):
            app.logger.warning("Invalid JUDGE0_LANGUAGE_IDS value. Expected JSON such as {\"racket\": 999}.")
    racket_id = os.getenv("JUDGE0_RACKET_LANGUAGE_ID", "").strip()
    if racket_id:
        try:
            language_ids["racket"] = int(racket_id)
        except ValueError:
            app.logger.warning("Invalid JUDGE0_RACKET_LANGUAGE_ID value: %s", racket_id)
    return language_ids


def judge0_headers() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "CodeBridge/1.0",
    }
    api_key = os.getenv("JUDGE0_API_KEY", "").strip()
    rapidapi_host = os.getenv("JUDGE0_RAPIDAPI_HOST", "").strip()
    if api_key and rapidapi_host:
        headers["X-RapidAPI-Key"] = api_key
        headers["X-RapidAPI-Host"] = rapidapi_host
    elif api_key:
        headers["X-Auth-Token"] = api_key
    return headers


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


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def touch_session_activity(store: dict, token: str, user: dict) -> None:
    session = store.get("sessions", {}).get(token)
    if not session:
        return
    now = datetime.now(timezone.utc)
    last_seen = parse_iso_datetime(session.get("lastSeenAt") or session.get("createdAt"))
    if (now - last_seen).total_seconds() < SESSION_TOUCH_SECONDS:
        return
    session["lastSeenAt"] = now.isoformat()
    user["lastActiveAt"] = session["lastSeenAt"]
    write_user_store(store)


def current_user() -> dict | None:
    token = request.cookies.get(USER_SESSION_COOKIE, "")
    if not token:
        return None
    store = read_user_store()
    session = store.get("sessions", {}).get(token)
    if not session:
        return None
    user = next((item for item in store["users"] if item["id"] == session.get("userId")), None)
    if user:
        touch_session_activity(store, token, user)
    return user


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
    now = utc_now_iso()
    store["sessions"][token] = {
        "userId": user["id"],
        "createdAt": now,
        "lastSeenAt": now,
    }
    user["lastActiveAt"] = now
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
            return "`#lang racket` selects the Racket language for this file. It is required at the top of a normal Racket file so the reader knows which grammar and libraries to use."
        if stripped.startswith(";"):
            return "Comment line. It explains code for a reader and does not run."
        if stripped.startswith("(define ("):
            return "Defines a function. The function name and parameters come after `define`."
        if stripped.startswith("(define "):
            if "(read-line)" in stripped:
                return "Runs `(read-line)` to get user text, then binds that result to a name with `define`."
            return "Binds a name to a value. Read `(define total (+ a b))` as: calculate `(+ a b)`, then name that result `total`."
        if stripped == "(displayln 42)":
            return "`(displayln 42)` calls `displayln` with the number `42`. `displayln` prints the value and adds a newline; parentheses are required because Racket calls look like `(function argument ...)`."
        if stripped.startswith("(displayln"):
            return "`displayln` produces output and moves to the next line. The first item after `(` is the function name; the rest is the value expression to print."
        if stripped.startswith("(display"):
            return "`display` produces output without adding a newline. It is useful for prompts before user input."
        if stripped.startswith("(printf"):
            return "`printf` prints formatted output. The format string controls where later values appear."
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


def run_with_judge0(target: str, source_code: str, stdin: str = "") -> dict:
    language_id = judge0_language_ids().get(target)
    if not language_id:
        return {
            "available": False,
            "status": "not_supported",
            "message": f"Judge0 is not configured for {target}. Public Judge0 CE currently covers Python, C, C++, and Java in this app.",
        }
    if len(source_code.encode("utf-8")) > 64 * 1024:
        return {
            "available": False,
            "status": "too_large",
            "message": "Code was not sent to Judge0 because it is larger than 64 KB.",
        }

    payload = {
        "source_code": source_code,
        "language_id": language_id,
        "stdin": stdin[:8000],
        "cpu_time_limit": 5,
        "wall_time_limit": 10,
        "memory_limit": 128000,
    }
    request_object = urllib.request.Request(
        f"{judge0_api_url()}/submissions?base64_encoded=false&wait=true",
        data=json.dumps(payload).encode("utf-8"),
        headers=judge0_headers(),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request_object, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:1200]
        return {
            "available": False,
            "status": "api_error",
            "message": f"Judge0 returned HTTP {error.code}: {body or error.reason}",
        }
    except Exception as error:
        return {
            "available": False,
            "status": "api_error",
            "message": f"Judge0 could not run this code: {error}",
        }

    status = result.get("status") or {}
    return {
        "available": True,
        "statusId": status.get("id"),
        "status": status.get("description", "Unknown"),
        "languageId": language_id,
        "stdout": result.get("stdout") or "",
        "stderr": result.get("stderr") or "",
        "compileOutput": result.get("compile_output") or "",
        "message": result.get("message") or "",
        "time": result.get("time"),
        "memory": result.get("memory"),
    }


def format_execution_result(result: dict) -> str:
    if not result.get("available"):
        return f"Judge0 code run: {result.get('message', 'Not available.')}"

    lines = [
        "Judge0 code run:",
        f"- Status: {result.get('status', 'Unknown')}",
    ]
    if result.get("time"):
        lines.append(f"- Time: {result['time']}s")
    if result.get("memory"):
        lines.append(f"- Memory: {result['memory']} KB")
    for label, key in (
        ("Stdout", "stdout"),
        ("Stderr", "stderr"),
        ("Compile output", "compileOutput"),
        ("Message", "message"),
    ):
        value = str(result.get(key) or "").strip()
        if value:
            lines.append(f"- {label}:\n{value[:4000]}")
    return "\n".join(lines)


def target_syntax_checks(target: str, code: str) -> list[tuple[str, bool]]:
    checks = {
        "racket": [
            ("Racket language line `#lang racket` or `#lang typed/racket`", "#lang racket" in code or "#lang typed/racket" in code),
            ("Racket prefix calls such as `(displayln value)` or `(+ a b)`", bool(re.search(r"\([A-Za-z+*/<>=!?-]+\s+", code))),
        ],
        "python": [
            ("Python output with `print(...)`", "print(" in code),
            ("Python avoids C++ braces for blocks", "{" not in code and "}" not in code),
            ("Python names avoid C-style declared types", not bool(re.search(r"\b(int|double|float|string|auto)\s+[A-Za-z_]\w*\s*=", code))),
        ],
        "cpp": [
            ("C++ include for standard library support", "#include" in code),
            ("C++ `main` entry point", "main(" in code),
            ("C++ output/input style such as `std::cout` or `std::cin`", "cout" in code or "cin" in code),
        ],
        "c": [
            ("C include for standard library support", "#include" in code),
            ("C `main` entry point", "main(" in code),
            ("C I/O style such as `printf` or `scanf`", "printf" in code or "scanf" in code),
        ],
        "java": [
            ("Java class or record wrapper", "class " in code or "record " in code),
            ("Java `main` entry point for runnable samples", "main(" in code),
            ("Java output with `System.out.println(...)`", "System.out.println" in code),
        ],
    }
    return checks.get(target, [])


def topic_construct_checks(base_kind: str, target: str, code: str) -> list[tuple[str, bool]]:
    lower = code.lower()
    checks = {
        "output": [("prints visible output", any(token in code for token in ("display", "print(", "printf", "cout", "System.out.println")))],
        "input": [("reads or simulates input", any(token in code for token in ("read-line", "input(", "scanf", "cin", "Scanner", "read ")))],
        "math": [("uses arithmetic calculation", any(token in code for token in ("+", "-", "*", "/", "%")))],
        "variable": [("creates named values", bool(re.search(r"(define\s+|=)", code)))],
        "if_statement": [("uses a conditional branch", "if" in lower)],
        "else_if": [("uses multi-branch logic", any(token in lower for token in ("else", "elif", "cond", "case", "switch")))],
        "error_check": [("checks invalid values before calculating", any(token in lower for token in ("if", "error", "invalid", "cannot")))],
        "while_loop": [("uses while-style repetition", any(token in lower for token in ("while", "let loop", "loop")))],
        "do_while": [("runs a menu or body at least once", any(token in lower for token in ("do", "while", "menu", "choice", "loop")))],
        "random_number": [("uses or simulates randomness", any(token in lower for token in ("random", "rand", "rng", "dice")))],
        "for_loop": [("uses counted or sequence repetition", any(token in lower for token in ("for", "range", "in-range")))],
        "nested_for": [("uses nested repetition", len(re.findall(r"\b(for|for\*|while)\b", lower)) >= 2 or "for*" in lower)],
        "function_intro": [("uses or explains a reusable function/helper", any(token in lower for token in ("def ", "define (", "function", "return", "helper")))],
        "create_function": [("defines a function", any(token in code for token in ("define (", "def ", "function ", "static ", "public static")))],
        "call_function": [("calls a function and uses returned value", bool(re.search(r"\w+\s*\(", code)) or bool(re.search(r"\(\w+[!?-]?\s+", code)))],
        "arrays_intro": [("uses a collection/list/array", any(token in lower for token in ("list", "vector", "array", "[", "{")))],
        "array_kinds": [("compares or uses collection types", any(token in lower for token in ("list", "vector", "array", "collection")))],
        "array_declare": [("declares and initializes a collection", any(token in lower for token in ("list", "vector", "array", "[", "{")))],
        "strings": [("uses string/text operations", any(token in lower for token in ("string", "str", "\"", "append", "length")))],
        "char_arrays": [("works with characters", any(token in lower for token in ("char", "character", "string-ref", "chars")))],
        "classes": [("defines a data type/class/struct", any(token in lower for token in ("class", "struct", "record")))],
        "switch_statement": [("uses exact-case branching", any(token in lower for token in ("switch", "case", "cond")))],
        "multi_arrays": [("uses nested collections or grid logic", any(token in lower for token in ("grid", "row", "column", "matrix", "list", "vector")))],
        "vectors": [("uses a vector/list-style sequence", any(token in lower for token in ("vector", "list", "array", "append", "push")))],
        "objects_classes": [("creates object/record values", any(token in lower for token in ("new ", "object", "struct", "class", "record")))],
        "recursion": [("uses a function that calls itself", (bool(re.search(r"(define\s+\((\w+)|def\s+(\w+)|\b(\w+)\s*\()", code)) and "return" in lower) or "recursive" in lower)],
        "search_float": [("searches data or uses decimals", any(token in lower for token in ("find", "search", "index", "float", "double", ".")))],
        "combined_if": [("combines conditions", any(token in lower for token in ("&&", "||", " and ", " or ", "and", "or")))],
        "nested_if": [("uses nested or staged decisions", lower.count("if") >= 2 or "cond" in lower)],
        "for_arrays": [("loops through a collection", any(token in lower for token in ("for", "map", "for/list", "foreach", "for-each")) and any(token in lower for token in ("list", "vector", "array", "[")))],
        "nested_for_multi": [("uses nested loops for rows and columns", len(re.findall(r"\b(for|for\*|while)\b", lower)) >= 2 or ("row" in lower and "col" in lower))],
        "while_validation": [("repeats until input is valid", any(token in lower for token in ("while", "loop", "valid", "invalid")))],
        "do_while_menu": [("uses menu-style repeated choices", any(token in lower for token in ("menu", "choice", "quit", "while", "do")))],
    }
    return checks.get(base_kind, [])


def analyze_code_submission(lesson: dict, content: str, execution: dict) -> dict:
    code = content.strip()
    target = lesson.get("target_language", "racket")
    base_kind = lesson.get("base_kind") or lesson.get("topic_kind", "")
    lines = [line for line in code.splitlines() if line.strip()]
    labels = sorted(set(re.findall(r"HW\s*Q\s*([123])", code, flags=re.IGNORECASE)))
    checks: list[dict] = []

    def add_check(name: str, passed: bool, fix: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "fix": fix})

    add_check("Non-empty submission", bool(code), "Upload a file or paste code.")
    add_check("Includes all three homework labels", len(labels) == 3, "Paste or label all three programs as HW Q1, HW Q2, and HW Q3.")
    add_check("Enough code for review", len(lines) >= 6, "Add complete programs, not only one or two lines.")
    add_check("Has at least one output line", any(token in code for token in ("display", "print(", "printf", "cout", "System.out.println")), "Print the required results so the checker can see behavior.")
    add_check("No obvious C++ leakage in target language", target in {"c", "cpp"} or ("#include" not in code and "std::" not in code), "Rewrite C++ syntax using the target language's normal form.")

    for name, passed in target_syntax_checks(target, code):
        add_check(name, passed, f"Revise this using normal {lesson.get('target_language_name', target)} syntax.")
    for name, passed in topic_construct_checks(base_kind, target, code):
        add_check(name, passed, f"Use the Day {lesson['day']} topic directly: {lesson['title']}.")

    if execution.get("available"):
        accepted = execution.get("statusId") == 3 or execution.get("status") == "Accepted"
        add_check("Runs successfully in Judge0", accepted, "Fix compile/runtime errors shown by Judge0 first.")
    else:
        message = execution.get("message", "Judge0 did not run this language.")
        runner_optional = "not configured" in message and target not in JUDGE0_DEFAULT_LANGUAGE_IDS
        add_check(
            "Judge0 run optional for this language" if runner_optional else "Judge0 run available",
            runner_optional,
            message,
        )

    passed_count = sum(1 for check in checks if check["passed"])
    score = round((passed_count / max(len(checks), 1)) * 10, 1)
    fixes = [check["fix"] for check in checks if not check["passed"]][:6]
    strengths = [check["name"] for check in checks if check["passed"]][:6]
    return {
        "score": score,
        "checks": checks,
        "strengths": strengths,
        "fixes": fixes,
        "programLabelsFound": labels,
        "nonEmptyLines": len(lines),
    }


def format_code_check_report(report: dict) -> str:
    lines = [
        "Built-in code checker:",
        f"- Score: {report.get('score', 0)}/10",
        f"- Non-empty lines: {report.get('nonEmptyLines', 0)}",
        f"- Homework labels found: {', '.join(report.get('programLabelsFound') or []) or 'none'}",
        "- Passed checks:",
    ]
    lines.extend(f"  - {item}" for item in report.get("strengths", []) or ["None yet"])
    lines.append("- Fix next:")
    lines.extend(f"  - {item}" for item in report.get("fixes", []) or ["Keep improving clarity and tests."])
    return "\n".join(lines)


def parse_iso_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)

def user_learning_guidance(user: dict, profile_override: dict | None = None) -> dict:
    profile = sanitize_profile(profile_override or user.get("profile", {}))
    target = normalize_target_language(profile.get("targetLanguage", "racket"))
    base = normalize_base_language(profile.get("baseLanguage") or "cpp")
    active_day = int(profile.get("activeDay", 1))
    lesson = get_lesson(active_day, target, base) or get_lesson(1, target, base)
    target_name = lesson.get("target_language_name", "target language")

    records = [
        record for record in read_submissions()
        if record.get("userId") == user["id"] and normalize_target_language(record.get("target", target)) == target
    ]
    records.sort(key=lambda item: parse_iso_datetime(item.get("createdAt")))
    submitted_days = {int(record.get("day", 0)) for record in records if str(record.get("day", "")).isdigit()}
    checker_reports = [record.get("codeCheck") or {} for record in records if record.get("codeCheck")]
    scores = [float(report.get("score", 0)) for report in checker_reports if isinstance(report.get("score"), (int, float))]
    average_score = round(sum(scores) / len(scores), 1) if scores else None

    failed_counts: dict[str, int] = {}
    missing_label_count = 0
    short_submission_count = 0
    runner_issue_count = 0
    for report in checker_reports:
        labels = report.get("programLabelsFound") or []
        if len(labels) < 3:
            missing_label_count += 1
        if int(report.get("nonEmptyLines") or 0) < 6:
            short_submission_count += 1
        for check in report.get("checks", []):
            if check.get("passed"):
                continue
            name = str(check.get("name", "Unclear issue"))
            failed_counts[name] = failed_counts.get(name, 0) + 1
            if "Judge0" in name or "Runs successfully" in name:
                runner_issue_count += 1

    common_failures = sorted(failed_counts.items(), key=lambda item: item[1], reverse=True)[:4]
    checklist_key = f"{target}.{active_day}"
    today_checks = profile.get("checklists", {}).get(checklist_key, [])
    checklist_done = sum(1 for item in today_checks if item)
    checklist_total = len(lesson.get("checklist", []))
    missing_previous = [day for day in range(1, active_day) if day not in submitted_days][:5]

    if not records:
        summary = (
            f"No homework has been submitted in the {target_name} track yet. "
            f"Start with Day {active_day:02d}, write HW Q1, HW Q2, and HW Q3 as separate programs, then submit once."
        )
    else:
        score_text = f" Average checker score: {average_score}/10." if average_score is not None else ""
        summary = (
            f"You have submitted {len(records)} homework record(s) across {len(submitted_days)} day(s) in {target_name}."
            f"{score_text} Current checklist: {checklist_done}/{checklist_total}."
        )

    today = [
        f"Day {active_day:02d}: {lesson['title']}. Study the bridge first, then code the three homework programs.",
        "Before coding, copy the exact numbers from HW Q1, HW Q2, and HW Q3 into comments so your output matches the task.",
        f"After coding, explain 3-6 important {target_name} lines with phrase-level notes: keyword/function, inputs, operator, result.",
    ]
    if missing_previous:
        today.append(f"Missing earlier submissions: Day {', Day '.join(str(day).zfill(2) for day in missing_previous)}. Review them before relying on later topics.")

    habits = []
    if missing_label_count:
        habits.append("You often miss HW labels. Put `HW Q1`, `HW Q2`, and `HW Q3` above each program.")
    if short_submission_count:
        habits.append("Some submissions are too short for strong review. Submit complete programs, not isolated lines.")
    if runner_issue_count:
        habits.append("Recent code runner checks found compile/runtime issues. Run the smallest program first, then add features.")
    if not habits:
        habits.append("Your current habit data is clean. Keep submitting labelled programs with visible output.")
    if checklist_total and checklist_done < checklist_total:
        habits.append("Checklist is not complete. Finish the unchecked items before moving your own study notes forward.")

    focus_areas = [
        f"{name}: failed {count} time(s)."
        for name, count in common_failures
    ] or [
        f"Phrase-level {target_name} syntax: explain what each token does before memorizing the full line.",
        "Clear output: every program should print labelled values and final result.",
    ]

    next_steps = [
        "First 10 minutes: read line-by-line notes and rewrite one sample line in your own words.",
        "Next 25 minutes: build HW Q1, HW Q2, and HW Q3 separately. Do not merge them into one vague program.",
        "Final 10 minutes: run code, check output, then submit with any question you want AI to focus on.",
    ]

    return {
        "summary": summary,
        "today": today,
        "habits": habits,
        "focusAreas": focus_areas,
        "nextSteps": next_steps,
        "stats": {
            "submissions": len(records),
            "submittedDays": len(submitted_days),
            "averageCheckerScore": average_score,
            "activeDay": active_day,
            "target": target,
        },
    }

def build_feedback_prompt(
    lesson: dict,
    content: str,
    student_note: str,
    execution_summary: str = "",
    code_check_summary: str = "",
) -> str:
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

Observed code runner result:
```text
{execution_summary or 'Code was not run.'}
```

Built-in code checker result:
```text
{code_check_summary or 'No built-in checker report.'}
```

Review in English. Use this exact structure:
1. Overall score out of 10.
2. Correctness feedback.
3. {target_language_name} style feedback, especially whether the code still follows {base_language_name} habits.
4. At least 5 concrete improvement points.
5. A recommended revised version or key revised snippet.
6. Which official documentation topic above the student should revisit.
7. Pick 3-6 important lines from the student's code and explain them line by line. For each selected line, explain important words or short phrases: keyword/function name, parentheses/braces/colon/semicolon, operators, values, variables, arguments, and result. Include the closest {base_language_name} comparison.
8. A checklist the student must complete before tomorrow's lesson.
Use the built-in code checker result as evidence. If the checker says HW labels, output, target syntax, or runner status failed, mention that directly.
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


def ai_feedback(
    lesson: dict,
    content: str,
    student_note: str,
    execution_summary: str = "",
    code_check_summary: str = "",
) -> str:
    prompt = build_feedback_prompt(lesson, content, student_note, execution_summary, code_check_summary)
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


@app.get("/admin-dashboard")
def admin_dashboard_page():
    return feedback_admin_page()


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


@app.post("/api/account/password")
@require_access
@require_user
def change_own_password():
    payload = request.get_json(silent=True) or {}
    current_password = str(payload.get("currentPassword", ""))
    new_password = str(payload.get("newPassword", ""))

    if len(new_password) < 8:
        return jsonify({"error": "new password must be at least 8 characters"}), 400
    if current_password == new_password:
        return jsonify({"error": "new password must be different from the current password"}), 400

    user = current_user()
    store = read_user_store()
    for stored_user in store["users"]:
        if stored_user["id"] == user["id"]:
            if not check_password_hash(stored_user.get("passwordHash", ""), current_password):
                return jsonify({"error": "current password is incorrect"}), 401
            stored_user["passwordHash"] = generate_password_hash(new_password)
            stored_user["passwordUpdatedAt"] = datetime.now(timezone.utc).isoformat()
            write_user_store(store)
            return jsonify({"ok": True, "user": public_user(stored_user)})

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


@app.get("/api/guidance")
@require_access
@require_user
def learning_guidance():
    user = current_user()
    profile = dict(user.get("profile", {}) or {})
    if request.args.get("day"):
        try:
            profile["activeDay"] = int(request.args["day"])
        except (TypeError, ValueError):
            pass
    if request.args.get("target"):
        profile["targetLanguage"] = request.args["target"]
    if request.args.get("base"):
        profile["baseLanguage"] = request.args["base"]
        profile["knownLanguages"] = [request.args["base"]] if request.args["base"] else []
        profile["languageExperienceChosen"] = True
    return jsonify({"guidance": user_learning_guidance(user, profile)})


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


def admin_user_dashboard_data() -> dict:
    store = read_user_store()
    users = store.get("users", [])
    user_ids = {user.get("id") for user in users}
    sessions = store.get("sessions", {})
    now = datetime.now(timezone.utc)
    submissions = read_submissions()
    submissions_by_user: dict[str, int] = {}
    for record in submissions:
        user_id = record.get("userId")
        if user_id:
            submissions_by_user[user_id] = submissions_by_user.get(user_id, 0) + 1

    sessions_by_user: dict[str, list[dict]] = {}
    active_sessions_by_user: dict[str, int] = {}
    for token, session in sessions.items():
        user_id = session.get("userId")
        if not user_id or user_id not in user_ids:
            continue
        session_record = dict(session)
        session_record["token"] = token
        sessions_by_user.setdefault(user_id, []).append(session_record)
        last_seen = parse_iso_datetime(session.get("lastSeenAt") or session.get("createdAt"))
        if (now - last_seen).total_seconds() <= ONLINE_WINDOW_SECONDS:
            active_sessions_by_user[user_id] = active_sessions_by_user.get(user_id, 0) + 1

    user_rows = []
    min_time = datetime.min.replace(tzinfo=timezone.utc)
    for user in users:
        profile = sanitize_profile(user.get("profile", {}))
        user_sessions = sessions_by_user.get(user["id"], [])
        session_times = [
            parse_iso_datetime(session.get("lastSeenAt") or session.get("createdAt"))
            for session in user_sessions
        ]
        stored_last_active = parse_iso_datetime(user.get("lastActiveAt") or user.get("createdAt"))
        last_active = max([stored_last_active, *session_times]) if session_times else stored_last_active
        active_session_count = active_sessions_by_user.get(user["id"], 0)
        user_rows.append({
            "id": user["id"],
            "name": user.get("name", "Unknown"),
            "isAdmin": is_admin_user(user),
            "role": "admin" if is_admin_user(user) else "student",
            "createdAt": user.get("createdAt"),
            "lastActiveAt": last_active.isoformat() if last_active != min_time else None,
            "online": active_session_count > 0,
            "sessionCount": len(user_sessions),
            "activeSessionCount": active_session_count,
            "submissions": submissions_by_user.get(user["id"], 0),
            "targetLanguage": profile.get("targetLanguage", "racket"),
            "baseLanguage": profile.get("baseLanguage", "") or "none",
            "activeDay": profile.get("activeDay", 1),
        })

    user_rows.sort(key=lambda item: (
        not item["online"],
        -(parse_iso_datetime(item.get("lastActiveAt")).timestamp()),
        item["name"].casefold(),
    ))
    online_users = sum(1 for item in user_rows if item["online"])
    active_sessions = sum(active_sessions_by_user.values())
    valid_sessions = sum(len(items) for items in sessions_by_user.values())
    return {
        "stats": {
            "totalRegistered": len(users),
            "onlineUsers": online_users,
            "activeSessions": active_sessions,
            "totalSessions": valid_sessions,
            "adminUsers": sum(1 for user in users if is_admin_user(user)),
            "onlineWindowMinutes": ONLINE_WINDOW_SECONDS // 60,
        },
        "users": user_rows,
    }


@app.get("/api/admin/users")
@require_access
@require_admin
def admin_users():
    return jsonify(admin_user_dashboard_data())


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
    stdin = request.form.get("stdin", "")
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

    execution = run_with_judge0(target, content, stdin)
    execution_summary = format_execution_result(execution)
    code_check = analyze_code_submission(lesson, content, execution)
    code_check_summary = format_code_check_report(code_check)
    feedback = "\n\n".join([
        execution_summary,
        code_check_summary,
        ai_feedback(lesson, content, student_note, execution_summary, code_check_summary),
    ])
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
        "stdin": stdin[:8000],
        "filename": saved_filename,
        "contentPreview": content[:1000],
        "content": content,
        "execution": execution,
        "codeCheck": code_check,
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
