from __future__ import annotations

import argparse
import json
import os
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
    "h",
    "hpp",
    "py",
    "json",
}

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
        return "没有检测到作业内容。请上传 .rkt 文件或粘贴代码后再请求批改。"

    target_language = lesson.get("target_language", "racket")
    if target_language == "racket" and "#lang racket" not in code and "#lang typed/racket" not in code:
        notes.append("建议在文件第一行加入 `#lang racket` 或对应语言声明。")
    if "(define" not in code and lesson["day"] >= 4:
        notes.append("今天之后的作业通常应该包含至少一个 `define`，用于练习命名和函数抽象。")
    if "check-" not in code and lesson["day"] >= 19:
        notes.append("从 Day 19 开始建议加入 rackunit 测试，例如 `check-equal?`。")
    if "for (" in code or "#include" in code:
        notes.append("看起来混入了 C++ 写法。尝试用递归、map/filter/fold 或表达式风格重写。")
    if lesson["day"] >= 9 and "(list" not in code and "cons" not in code and "empty?" not in code:
        notes.append("今天已经进入列表主题，建议在作业里体现 list/cons/empty? 等核心操作。")
    if len(lines) < 8:
        notes.append("代码量偏少。建议补充更多例子、测试或解释注释，证明你理解了今日主题。")
    if not notes:
        notes.append("基础结构不错。下一步可以提升命名、测试覆盖和边界情况处理。")

    return (
        "本地规则反馈：\n"
        f"- 今日主题：{lesson['category']} - {lesson['title']}\n"
        f"- 检测到非空代码行：{len(lines)} 行\n"
        + "\n".join(f"- {note}" for note in notes)
        + "\n\n配置 OPENAI_API_KEY 后，可以获得更细的 AI 批改，包括逐段解释和改进建议。"
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
    prompt = f"""
你是一位严格但友好的编程老师。学生有 C++ 基础，正在按照 56 天课程学习 {lesson.get('target_language_name', 'Racket')}。

今日课程：
Day {lesson['day']}: {lesson['title']}
Category: {lesson['category']}
目标：{lesson['goal']}
C++ 对照：{lesson['cpp_bridge']}
今日作业：{lesson['assignment']}
评分标准：{'; '.join(lesson['grading_rubric'])}

今天的 C++ 到 Racket 语法迁移重点：
概念：{syntax_bridge.get('concept', '无')}
迁移角度：{syntax_bridge.get('today_angle', '无')}
C++ 写法：
```cpp
{syntax_bridge.get('cpp', '')}
```
Racket 写法：
```racket
{syntax_bridge.get('racket', '')}
```
迁移步骤：{'; '.join(syntax_bridge.get('translation_steps', []))}
常见误区：{'; '.join(syntax_bridge.get('pitfalls', []))}
官方文档：
{doc_lines}

学生备注：
{student_note or '无'}

学生提交：
```racket
{content[:12000]}
```

请用中文批改。结构必须包含：
1. 总体评分，满分 10 分。
2. 正确性反馈。
3. {lesson.get('target_language_name', 'Racket')} 风格反馈，尤其指出是否还在用 C++ 思维。
4. 具体可改进点，至少 5 条。
5. 推荐修改版本或关键片段。
6. 结合上方官方文档链接，指出学生应该回看哪个文档主题。
7. 明天学习前必须补齐的 checklist。
不要编造未看到的运行结果；如果需要运行测试，请明确告诉学生怎么运行。
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
    return jsonify({"submissions": list(reversed(read_submissions()))})


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
