from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, request, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from course_data import (
    get_course_length,
    get_language_options,
    get_lesson,
    get_lessons,
    normalize_base_language,
    normalize_target_language,
    normalize_ui_language,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data")).expanduser()
UPLOAD_DIR = DATA_DIR / "uploads"
SUBMISSIONS_FILE = DATA_DIR / "submissions.json"
USERS_FILE = DATA_DIR / "users.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
USER_SESSION_COOKIE = "code_tutor_session"
ONLINE_WINDOW_SECONDS = 15 * 60
SESSION_TOUCH_SECONDS = 30
SUPPORTED_UI_LANGUAGES = {"en", "zh", "ja", "ko", "fr"}
POP_QUIZ_INTERVAL_DAYS = (1, 3, 7, 14, 30)
POP_QUIZ_FIXED_TIME = "20:00"
POP_QUIZ_MEMORY_CURVE = "1, 3, 7, 14, 30"
DEFAULT_TIME_ZONE = "UTC"
GUIDANCE_TEXT = {
    "en": {
        "no_homework": "No homework has been submitted in the {target_name} track yet. Start with Day {day:02d}, write HW Q1, HW Q2, and HW Q3 as separate programs, then submit once.",
        "summary": "You have submitted {records} homework record(s) across {days} day(s) in {target_name}.{score_text}{mastery_text} Current checklist: {done}/{total}.",
        "score_text": " Average checker score: {score}/10.",
        "mastery_text": " Average mastery: {rating}/5 across {count} rated lesson(s).",
        "today_1": "Day {day:02d}: {title}. Study the bridge first, then code the three homework programs.",
        "today_2": "Before coding, copy the exact numbers from HW Q1, HW Q2, and HW Q3 into comments so your output matches the task.",
        "today_3": "After coding, explain 3-6 important {target_name} lines with phrase-level notes: keyword/function, inputs, operator, result.",
        "missing_previous": "Missing earlier submissions: Day {days}. Review them before relying on later topics.",
        "habit_labels": "You often miss HW labels. Put `HW Q1`, `HW Q2`, and `HW Q3` above each program.",
        "habit_short": "Some submissions are too short for strong review. Submit complete programs, not isolated lines.",
        "habit_runner": "Recent code runner checks found compile/runtime issues. Run the smallest program first, then add features.",
        "habit_clean": "Your current habit data is clean. Keep submitting labelled programs with visible output.",
        "habit_checklist": "Checklist is not complete. Finish the unchecked items before moving your own study notes forward.",
        "focus_failed": "{name}: failed {count} time(s).",
        "focus_syntax": "Phrase-level {target_name} syntax: explain what each token does before memorizing the full line.",
        "focus_output": "Clear output: every program should print labelled values and final result.",
        "weakest_focus": "Weakest knowledge: Day {day:02d} - {title} ({rating}/5, {label}). Reinforce this before new lessons.",
        "pop_quiz_due": "POP quiz due {date} at {time}: Day {day:02d} after {interval} day(s).",
        "pop_quiz_plan": "POP quizzes run at {time} on memory-curve checkpoints: {curve} day(s) after each submitted homework.",
        "pop_quiz_next": "Next POP quiz: {date} at {time}, Day {day:02d} - {title}.",
        "next_1": "First 10 minutes: read line-by-line notes and rewrite one sample line in your own words.",
        "next_2": "Next 25 minutes: build HW Q1, HW Q2, and HW Q3 separately. Do not merge them into one vague program.",
        "next_3": "Final 10 minutes: run code, check output, then submit with any question you want AI to focus on.",
        "feedback_language": "English",
    },
    "zh": {
        "no_homework": "{target_name} 课程还没有提交作业。请从第 {day:02d} 天开始，把 HW Q1、HW Q2 和 HW Q3 写成三个独立程序，然后提交一次。",
        "summary": "你已经在 {target_name} 中提交了 {records} 条作业记录，覆盖 {days} 天。{score_text}{mastery_text} 当前清单：{done}/{total}。",
        "score_text": " 平均检查器分数：{score}/10。",
        "mastery_text": " 平均掌握度：{rating}/5，共 {count} 个已评分课程。",
        "today_1": "第 {day:02d} 天：{title}。先学习桥梁内容，再编写三个作业程序。",
        "today_2": "写代码前，把 HW Q1、HW Q2 和 HW Q3 的具体数字复制到注释里，确保输出匹配任务。",
        "today_3": "写完后，解释 3-6 行重要的 {target_name} 代码，说明关键字/函数、输入、运算符和结果。",
        "missing_previous": "缺少之前提交：第 {days} 天。继续依赖后续主题前，请先回顾这些内容。",
        "habit_labels": "你经常缺少 HW 标签。请在每个程序上方写 `HW Q1`、`HW Q2` 和 `HW Q3`。",
        "habit_short": "有些提交太短，难以深入批改。请提交完整程序，而不是零散代码行。",
        "habit_runner": "最近运行检查发现编译或运行问题。先运行最小程序，再添加功能。",
        "habit_clean": "目前学习习惯数据正常。继续提交带标签、能看见输出的程序。",
        "habit_checklist": "清单还没有完成。请先完成未勾选项，再推进自己的学习笔记。",
        "focus_failed": "{name}：失败 {count} 次。",
        "focus_syntax": "{target_name} 短语级语法：先说明每个 token 做什么，再记整行。",
        "focus_output": "清晰输出：每个程序都应该打印带标签的值和最终结果。",
        "weakest_focus": "最薄弱知识点：第 {day:02d} 天 - {title}（{rating}/5，{label}）。继续学新课前请先加强这里。",
        "pop_quiz_due": "POP 小测：{date} {time}，复习第 {day:02d} 天，间隔 {interval} 天后。",
        "pop_quiz_plan": "POP 小测固定在 {time}，按记忆曲线安排：每次提交作业后第 {curve} 天复习。",
        "pop_quiz_next": "下一次 POP 小测：{date} {time}，第 {day:02d} 天 - {title}。",
        "next_1": "前 10 分钟：阅读逐行笔记，并用自己的话改写一行示例。",
        "next_2": "接下来 25 分钟：分别完成 HW Q1、HW Q2 和 HW Q3。不要合并成一个模糊程序。",
        "next_3": "最后 10 分钟：运行代码、检查输出，然后带着希望 AI 关注的问题提交。",
        "feedback_language": "Chinese",
    },
    "ja": {
        "no_homework": "{target_name} トラックにはまだ宿題が提出されていません。{day:02d}日目から始め、HW Q1、HW Q2、HW Q3 を別々のプログラムとして書き、1 回提出してください。",
        "summary": "{target_name} で {records} 件の宿題記録を提出し、{days} 日分をカバーしています。{score_text}{mastery_text} 現在のチェックリスト：{done}/{total}。",
        "score_text": " 平均チェッカースコア：{score}/10。",
        "mastery_text": " 平均習熟度：{rating}/5、評価済みレッスン {count} 件。",
        "today_1": "{day:02d}日目：{title}。まずブリッジを学び、その後 3 つの宿題プログラムを書きます。",
        "today_2": "コーディング前に、HW Q1、HW Q2、HW Q3 の具体的な数値をコメントにコピーし、出力が課題に合うようにします。",
        "today_3": "コーディング後、重要な {target_name} の行を 3-6 行選び、キーワード/関数、入力、演算子、結果を短く説明します。",
        "missing_previous": "未提出の前の課題：{days}日目。後の内容に進む前に復習してください。",
        "habit_labels": "HW ラベルが抜けることがあります。各プログラムの上に `HW Q1`、`HW Q2`、`HW Q3` を置いてください。",
        "habit_short": "一部の提出は短すぎて十分にレビューできません。断片ではなく完全なプログラムを提出してください。",
        "habit_runner": "最近の実行チェックでコンパイル/実行の問題が見つかりました。まず最小プログラムを動かしてから機能を追加してください。",
        "habit_clean": "現在の学習習慣データは良好です。ラベル付きで見える出力のあるプログラムを提出し続けてください。",
        "habit_checklist": "チェックリストが完了していません。未チェック項目を終えてから学習ノートを進めてください。",
        "focus_failed": "{name}：{count} 回失敗。",
        "focus_syntax": "{target_name} のフレーズ単位の構文：行全体を覚える前に各 token の役割を説明します。",
        "focus_output": "明確な出力：すべてのプログラムでラベル付きの値と最終結果を出力してください。",
        "weakest_focus": "最も弱い知識：{day:02d}日目 - {title}（{rating}/5、{label}）。新しいレッスン前にここを補強してください。",
        "pop_quiz_due": "POP クイズ：{date} {time}、{interval} 日後に {day:02d}日目を復習。",
        "pop_quiz_plan": "POP クイズは {time} 固定で、提出後 {curve} 日目の記憶曲線チェックポイントに沿って行います。",
        "pop_quiz_next": "次の POP クイズ：{date} {time}、{day:02d}日目 - {title}。",
        "next_1": "最初の 10 分：行ごとのノートを読み、サンプル行を自分の言葉で書き直します。",
        "next_2": "次の 25 分：HW Q1、HW Q2、HW Q3 を別々に作ります。あいまいな 1 つのプログラムにまとめないでください。",
        "next_3": "最後の 10 分：コードを実行し、出力を確認し、AI に見てほしい質問と一緒に提出します。",
        "feedback_language": "Japanese",
    },
    "ko": {
        "no_homework": "{target_name} 트랙에는 아직 제출된 숙제가 없습니다. {day:02d}일차부터 시작해 HW Q1, HW Q2, HW Q3를 별도 프로그램으로 작성한 뒤 한 번 제출하세요.",
        "summary": "{target_name}에서 {records}개의 숙제 기록을 제출했고 {days}일을 다뤘습니다. {score_text}{mastery_text} 현재 체크리스트: {done}/{total}.",
        "score_text": " 평균 검사 점수: {score}/10.",
        "mastery_text": " 평균 숙련도: {rating}/5, 평가된 수업 {count}개.",
        "today_1": "{day:02d}일차: {title}. 먼저 연결 내용을 공부한 뒤 세 개의 숙제 프로그램을 작성하세요.",
        "today_2": "코딩 전 HW Q1, HW Q2, HW Q3의 정확한 숫자를 주석에 복사해 출력이 과제와 맞도록 하세요.",
        "today_3": "코딩 후 중요한 {target_name} 줄 3-6개를 골라 키워드/함수, 입력, 연산자, 결과를 짧게 설명하세요.",
        "missing_previous": "이전 제출 누락: {days}일차. 이후 주제에 의존하기 전에 복습하세요.",
        "habit_labels": "HW 라벨을 자주 빠뜨립니다. 각 프로그램 위에 `HW Q1`, `HW Q2`, `HW Q3`를 넣으세요.",
        "habit_short": "일부 제출은 너무 짧아 강한 검토가 어렵습니다. 단독 줄이 아니라 완성된 프로그램을 제출하세요.",
        "habit_runner": "최근 실행 검사에서 컴파일/런타임 문제가 발견되었습니다. 가장 작은 프로그램을 먼저 실행한 뒤 기능을 추가하세요.",
        "habit_clean": "현재 학습 습관 데이터가 좋습니다. 라벨이 있고 출력이 보이는 프로그램을 계속 제출하세요.",
        "habit_checklist": "체크리스트가 완료되지 않았습니다. 체크하지 않은 항목을 끝낸 뒤 학습 노트를 진행하세요.",
        "focus_failed": "{name}: {count}회 실패.",
        "focus_syntax": "{target_name} 구문 단위 문법: 전체 줄을 외우기 전에 각 token의 역할을 설명하세요.",
        "focus_output": "명확한 출력: 모든 프로그램은 라벨이 있는 값과 최종 결과를 출력해야 합니다.",
        "weakest_focus": "가장 약한 지식: {day:02d}일차 - {title}({rating}/5, {label}). 새 수업 전에 이 부분을 강화하세요.",
        "pop_quiz_due": "POP 퀴즈: {date} {time}, {interval}일 후 {day:02d}일차 복습.",
        "pop_quiz_plan": "POP 퀴즈는 {time}에 고정되며, 제출 후 {curve}일 기억 곡선 체크포인트에 맞춰 진행됩니다.",
        "pop_quiz_next": "다음 POP 퀴즈: {date} {time}, {day:02d}일차 - {title}.",
        "next_1": "처음 10분: 줄별 노트를 읽고 예제 한 줄을 자신의 말로 다시 씁니다.",
        "next_2": "다음 25분: HW Q1, HW Q2, HW Q3를 각각 만듭니다. 하나의 모호한 프로그램으로 합치지 마세요.",
        "next_3": "마지막 10분: 코드를 실행하고 출력을 확인한 뒤 AI가 봐 주길 원하는 질문과 함께 제출하세요.",
        "feedback_language": "Korean",
    },
    "fr": {
        "no_homework": "Aucun devoir n'a encore été soumis dans le parcours {target_name}. Commencez par le jour {day:02d}, écrivez HW Q1, HW Q2 et HW Q3 comme programmes séparés, puis soumettez une fois.",
        "summary": "Vous avez soumis {records} devoir(s) sur {days} jour(s) en {target_name}.{score_text}{mastery_text} Liste actuelle : {done}/{total}.",
        "score_text": " Score moyen du vérificateur : {score}/10.",
        "mastery_text": " Maîtrise moyenne : {rating}/5 sur {count} leçon(s) évaluée(s).",
        "today_1": "Jour {day:02d} : {title}. Étudiez d'abord le pont, puis codez les trois programmes de devoir.",
        "today_2": "Avant de coder, copiez les nombres exacts de HW Q1, HW Q2 et HW Q3 dans des commentaires pour que la sortie corresponde à la tâche.",
        "today_3": "Après le codage, expliquez 3 à 6 lignes importantes de {target_name} au niveau des expressions : mot-clé/fonction, entrées, opérateur, résultat.",
        "missing_previous": "Soumissions précédentes manquantes : jour {days}. Révisez-les avant de vous appuyer sur les sujets suivants.",
        "habit_labels": "Les étiquettes HW manquent souvent. Placez `HW Q1`, `HW Q2` et `HW Q3` au-dessus de chaque programme.",
        "habit_short": "Certaines soumissions sont trop courtes pour une bonne correction. Soumettez des programmes complets, pas des lignes isolées.",
        "habit_runner": "Les vérifications récentes ont trouvé des erreurs de compilation/exécution. Exécutez d'abord le plus petit programme, puis ajoutez les fonctionnalités.",
        "habit_clean": "Vos données d'habitude sont propres. Continuez à soumettre des programmes étiquetés avec une sortie visible.",
        "habit_checklist": "La liste n'est pas complète. Terminez les éléments non cochés avant d'avancer vos notes.",
        "focus_failed": "{name} : échoué {count} fois.",
        "focus_syntax": "Syntaxe {target_name} au niveau des expressions : expliquez chaque token avant de mémoriser la ligne.",
        "focus_output": "Sortie claire : chaque programme doit afficher des valeurs étiquetées et le résultat final.",
        "weakest_focus": "Point le plus faible : jour {day:02d} - {title} ({rating}/5, {label}). Renforcez-le avant les nouvelles leçons.",
        "pop_quiz_due": "Quiz POP prévu le {date} à {time} : jour {day:02d} après {interval} jour(s).",
        "pop_quiz_plan": "Les quiz POP ont lieu à {time}, selon les points de la courbe de mémoire : {curve} jour(s) après chaque devoir soumis.",
        "pop_quiz_next": "Prochain quiz POP : {date} à {time}, jour {day:02d} - {title}.",
        "next_1": "Premières 10 minutes : lisez les notes ligne par ligne et reformulez une ligne d'exemple.",
        "next_2": "25 minutes suivantes : construisez HW Q1, HW Q2 et HW Q3 séparément. Ne les fusionnez pas en un programme vague.",
        "next_3": "10 dernières minutes : exécutez le code, vérifiez la sortie, puis soumettez avec la question à poser à l'IA.",
        "feedback_language": "French",
    },
}
JUDGE0_DEFAULT_URL = "https://ce.judge0.com"
JUDGE0_DEFAULT_LANGUAGE_IDS = {
    "c": 103,
    "cpp": 105,
    "java": 91,
    "python": 109,
    "r": 99,
}
ALLOWED_EXTENSIONS = {
    "r",
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
    r_id = os.getenv("JUDGE0_R_LANGUAGE_ID", "").strip()
    if r_id:
        try:
            language_ids["r"] = int(r_id)
        except ValueError:
            app.logger.warning("Invalid JUDGE0_R_LANGUAGE_ID value: %s", r_id)
    return language_ids


def judge0_headers() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "CODEBRIDGE/1.0",
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
        "uiLanguage": "en",
        "timeZone": DEFAULT_TIME_ZONE,
        "activeDay": 1,
        "checklists": {},
    }


def normalize_time_zone(value: str | None) -> str:
    zone = str(value or DEFAULT_TIME_ZONE).strip() or DEFAULT_TIME_ZONE
    try:
        ZoneInfo(zone)
        return zone
    except ZoneInfoNotFoundError:
        return DEFAULT_TIME_ZONE


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
    allowed_languages = {"cpp", "racket", "python", "java", "c", "r"}
    known = [item for item in profile.get("knownLanguages", []) if item in allowed_languages]
    raw_base = str(profile.get("baseLanguage") or "").strip().lower()
    language_experience_chosen = bool(profile.get("languageExperienceChosen"))
    if "languageExperienceChosen" not in profile and (known or raw_base in allowed_languages):
        language_experience_chosen = True
    target = normalize_target_language(profile.get("targetLanguage", "racket"))
    ui_language = str(profile.get("uiLanguage") or "en").strip().lower()
    if ui_language not in SUPPORTED_UI_LANGUAGES:
        ui_language = "en"
    time_zone = normalize_time_zone(profile.get("timeZone"))
    max_day = get_course_length(target)
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
        "uiLanguage": ui_language,
        "timeZone": time_zone,
        "activeDay": max(1, min(active_day, max_day)),
        "checklists": checklists,
    }


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def read_uploaded_text(path: Path) -> str:
    raw = path.read_bytes()
    return raw.decode("utf-8", errors="replace")


LOCAL_FEEDBACK_TEXT = {
    "en": {
        "empty": "No assignment content was detected. Upload a file or paste code before requesting feedback.",
        "racket_lang": "For Racket, put `#lang racket` or `#lang typed/racket` on the first line.",
        "racket_define": "After Day 4, most Racket assignments should include at least one `define` for naming or abstraction practice.",
        "racket_tests": "From Day 19 onward, add rackunit tests such as `check-equal?` when possible.",
        "python_def": "For Python function days, include at least one `def` so the work practices function design.",
        "c_include": "For C, include the relevant headers, such as `#include <stdio.h>` for formatted output.",
        "cpp_main": "For early C++ foundation lessons, include a small `main` function so the program can run from the command line.",
        "java_class": "For Java, place the code inside a class or record so it matches normal Java structure.",
        "r_syntax": "For R, use normal R syntax such as `<-` assignments, `cat(...)` output, or `function(...)` definitions.",
        "cpp_leak": "The submission still contains C++ syntax. Rewrite that part using the target language's normal idioms.",
        "short": "This is a short submission, so the review focuses on every submitted line. Short code can still receive useful syntax and logic feedback.",
        "reasonable": "The basic structure looks reasonable. Next, improve naming, test coverage, and edge-case handling.",
        "line_empty": "No non-empty lines were available for line-by-line review.",
        "title": "Local rule-based feedback:",
        "lesson": "Lesson",
        "target_language": "Target language",
        "non_empty": "Non-empty code lines detected",
        "line_review": "Line-by-line quick review:",
        "closing": "This review used the built-in checker. Use the notes above to revise the program, then submit again for another pass.",
        "generic_line": "This line should be checked against the lesson goal, surrounding block, and expected output.",
        "checker_title": "Built-in code checker:",
        "score": "Score",
        "mastery": "Mastery rating",
        "non_empty_lines": "Non-empty lines",
        "labels": "Homework labels found",
        "passed": "Passed checks",
        "fix_next": "Fix next",
        "none": "none",
        "none_yet": "None yet",
        "keep_improving": "Keep improving clarity and tests.",
    },
    "zh": {
        "empty": "没有检测到作业内容。请上传文件或粘贴代码后再请求批改。",
        "racket_lang": "Racket 程序第一行请写 `#lang racket` 或 `#lang typed/racket`。",
        "racket_define": "第 4 天之后，大多数 Racket 作业应至少包含一个 `define`，用来练习命名或抽象。",
        "racket_tests": "第 19 天之后，尽量加入 rackunit 测试，例如 `check-equal?`。",
        "python_def": "Python 函数主题中，请至少包含一个 `def` 来练习函数设计。",
        "c_include": "C 程序请包含相关头文件，例如格式化输出需要 `#include <stdio.h>`。",
        "cpp_main": "早期 C++ 基础课程请包含一个小的 `main` 函数，让程序能从命令行运行。",
        "java_class": "Java 代码请放进 class 或 record 中，符合正常 Java 结构。",
        "r_syntax": "R 代码请使用正常 R 语法，例如 `<-` 赋值、`cat(...)` 输出或 `function(...)` 定义。",
        "cpp_leak": "提交中仍包含 C++ 语法。请用目标语言的正常写法重写这部分。",
        "short": "这次提交较短，所以批改会集中检查每一行。短代码仍然可以得到有用的语法和逻辑反馈。",
        "reasonable": "基本结构看起来合理。下一步请改进命名、测试覆盖和边界情况处理。",
        "line_empty": "没有可用于逐行批改的非空代码行。",
        "title": "本地规则批改：",
        "lesson": "课程",
        "target_language": "目标语言",
        "non_empty": "检测到的非空代码行",
        "line_review": "逐行快速批改：",
        "closing": "这次批改使用了内置检查器。请根据上面的说明修改程序，然后再次提交。",
        "generic_line": "这一行需要结合课程目标、上下文代码块和预期输出一起检查。",
        "checker_title": "内置代码检查器：",
        "score": "分数",
        "mastery": "掌握度",
        "non_empty_lines": "非空代码行",
        "labels": "找到的作业标签",
        "passed": "已通过检查",
        "fix_next": "下一步修改",
        "none": "无",
        "none_yet": "暂时没有",
        "keep_improving": "继续改进清晰度和测试。",
    },
    "ja": {
        "empty": "課題内容が検出されませんでした。ファイルをアップロードするかコードを貼り付けてからレビューを依頼してください。",
        "racket_lang": "Racket では最初の行に `#lang racket` または `#lang typed/racket` を置いてください。",
        "racket_define": "4 日目以降の Racket 課題では、命名や抽象化の練習として少なくとも 1 つの `define` を含めてください。",
        "racket_tests": "19 日目以降は、可能なら `check-equal?` などの rackunit テストを追加してください。",
        "python_def": "Python の関数の日では、関数設計を練習するため少なくとも 1 つの `def` を含めてください。",
        "c_include": "C では、整形出力なら `#include <stdio.h>` など必要なヘッダーを含めてください。",
        "cpp_main": "初期の C++ 基礎課題では、コマンドラインから実行できる小さな `main` 関数を含めてください。",
        "java_class": "Java では、通常の構造に合わせてコードを class または record の中に置いてください。",
        "r_syntax": "R では `<-` 代入、`cat(...)` 出力、`function(...)` 定義など通常の R 構文を使ってください。",
        "cpp_leak": "提出にはまだ C++ 構文が含まれています。目標言語の通常の書き方に直してください。",
        "short": "今回の提出は短いため、レビューは提出された各行に集中します。短いコードでも有用な構文とロジックのフィードバックを受けられます。",
        "reasonable": "基本構造は妥当に見えます。次に名前付け、テスト範囲、境界ケースを改善してください。",
        "line_empty": "行ごとのレビューに使える非空行がありませんでした。",
        "title": "ローカル規則ベースのフィードバック：",
        "lesson": "レッスン",
        "target_language": "目標言語",
        "non_empty": "検出された非空コード行",
        "line_review": "行ごとのクイックレビュー：",
        "closing": "このレビューは内蔵チェッカーを使用しました。上のメモを使ってプログラムを修正し、もう一度提出してください。",
        "generic_line": "この行は、レッスン目標、周囲のブロック、期待される出力と照らして確認してください。",
        "checker_title": "内蔵コードチェッカー：",
        "score": "スコア",
        "mastery": "習熟度",
        "non_empty_lines": "非空行",
        "labels": "見つかった宿題ラベル",
        "passed": "合格したチェック",
        "fix_next": "次に直すこと",
        "none": "なし",
        "none_yet": "まだありません",
        "keep_improving": "明確さとテストをさらに改善してください。",
    },
    "ko": {
        "empty": "과제 내용이 감지되지 않았습니다. 파일을 업로드하거나 코드를 붙여넣은 뒤 피드백을 요청하세요.",
        "racket_lang": "Racket은 첫 줄에 `#lang racket` 또는 `#lang typed/racket`을 넣으세요.",
        "racket_define": "4일차 이후 대부분의 Racket 과제에는 이름짓기나 추상화 연습을 위해 최소 하나의 `define`이 있어야 합니다.",
        "racket_tests": "19일차 이후에는 가능하면 `check-equal?` 같은 rackunit 테스트를 추가하세요.",
        "python_def": "Python 함수 주제에서는 함수 설계를 연습하도록 최소 하나의 `def`를 포함하세요.",
        "c_include": "C에서는 형식화 출력에 필요한 `#include <stdio.h>` 같은 관련 헤더를 포함하세요.",
        "cpp_main": "초기 C++ 기초 과제에서는 명령줄에서 실행할 수 있도록 작은 `main` 함수를 포함하세요.",
        "java_class": "Java에서는 정상적인 Java 구조에 맞게 코드를 class 또는 record 안에 넣으세요.",
        "r_syntax": "R에서는 `<-` 대입, `cat(...)` 출력, `function(...)` 정의 같은 정상적인 R 문법을 사용하세요.",
        "cpp_leak": "제출물에 아직 C++ 문법이 포함되어 있습니다. 목표 언어의 일반적인 방식으로 다시 작성하세요.",
        "short": "이번 제출은 짧기 때문에 리뷰는 제출된 각 줄에 집중합니다. 짧은 코드도 유용한 문법과 논리 피드백을 받을 수 있습니다.",
        "reasonable": "기본 구조는 괜찮아 보입니다. 다음에는 이름짓기, 테스트 범위, 경계 사례 처리를 개선하세요.",
        "line_empty": "줄별 리뷰에 사용할 비어 있지 않은 코드 줄이 없습니다.",
        "title": "로컬 규칙 기반 피드백:",
        "lesson": "수업",
        "target_language": "목표 언어",
        "non_empty": "감지된 비어 있지 않은 코드 줄",
        "line_review": "줄별 빠른 리뷰:",
        "closing": "이 리뷰는 내장 검사기를 사용했습니다. 위 메모를 바탕으로 프로그램을 수정한 뒤 다시 제출하세요.",
        "generic_line": "이 줄은 수업 목표, 주변 블록, 예상 출력과 함께 확인해야 합니다.",
        "checker_title": "내장 코드 검사기:",
        "score": "점수",
        "mastery": "숙련도",
        "non_empty_lines": "비어 있지 않은 줄",
        "labels": "찾은 숙제 라벨",
        "passed": "통과한 검사",
        "fix_next": "다음 수정",
        "none": "없음",
        "none_yet": "아직 없음",
        "keep_improving": "명확성과 테스트를 계속 개선하세요.",
    },
    "fr": {
        "empty": "Aucun contenu de devoir n'a été détecté. Téléversez un fichier ou collez du code avant de demander une correction.",
        "racket_lang": "Pour Racket, mettez `#lang racket` ou `#lang typed/racket` sur la première ligne.",
        "racket_define": "Après le jour 4, la plupart des devoirs Racket doivent inclure au moins un `define` pour pratiquer le nommage ou l'abstraction.",
        "racket_tests": "À partir du jour 19, ajoutez si possible des tests rackunit comme `check-equal?`.",
        "python_def": "Pour les jours de fonctions Python, incluez au moins un `def` afin de pratiquer la conception de fonctions.",
        "c_include": "En C, incluez les en-têtes nécessaires, par exemple `#include <stdio.h>` pour la sortie formatée.",
        "cpp_main": "Dans les premières leçons C++, incluez une petite fonction `main` pour que le programme puisse s'exécuter en ligne de commande.",
        "java_class": "En Java, placez le code dans une classe ou un record pour respecter la structure normale.",
        "r_syntax": "En R, utilisez une syntaxe normale comme les affectations `<-`, la sortie `cat(...)` ou les définitions `function(...)`.",
        "cpp_leak": "La soumission contient encore de la syntaxe C++. Réécrivez cette partie avec les idiomes du langage cible.",
        "short": "Cette soumission est courte ; la correction se concentre donc sur chaque ligne envoyée. Un code court peut quand même recevoir des conseils utiles.",
        "reasonable": "La structure de base semble raisonnable. Améliorez ensuite les noms, les tests et les cas limites.",
        "line_empty": "Aucune ligne non vide n'était disponible pour la correction ligne par ligne.",
        "title": "Correction locale par règles :",
        "lesson": "Leçon",
        "target_language": "Langage cible",
        "non_empty": "Lignes de code non vides détectées",
        "line_review": "Correction rapide ligne par ligne :",
        "closing": "Cette correction a utilisé le vérificateur intégré. Utilisez les notes ci-dessus pour réviser le programme, puis soumettez à nouveau.",
        "generic_line": "Cette ligne doit être vérifiée par rapport à l'objectif, au bloc environnant et à la sortie attendue.",
        "checker_title": "Vérificateur de code intégré :",
        "score": "Score",
        "mastery": "Niveau de maîtrise",
        "non_empty_lines": "Lignes non vides",
        "labels": "Étiquettes de devoir trouvées",
        "passed": "Vérifications réussies",
        "fix_next": "À corriger ensuite",
        "none": "aucun",
        "none_yet": "Aucune pour le moment",
        "keep_improving": "Continuez à améliorer la clarté et les tests.",
    },
}


def local_feedback_text(ui_language: str) -> dict:
    return LOCAL_FEEDBACK_TEXT.get(normalize_ui_language(ui_language), LOCAL_FEEDBACK_TEXT["en"])


MASTERY_LABELS = {
    "en": {
        1: "not mastered",
        2: "weak",
        3: "developing",
        4: "mostly mastered",
        5: "fully mastered",
    },
    "zh": {
        1: "未掌握",
        2: "较弱",
        3: "正在发展",
        4: "基本掌握",
        5: "完全掌握",
    },
    "ja": {
        1: "未習得",
        2: "弱い",
        3: "発展中",
        4: "ほぼ習得",
        5: "完全に習得",
    },
    "ko": {
        1: "미숙",
        2: "약함",
        3: "발전 중",
        4: "대체로 숙달",
        5: "완전히 숙달",
    },
    "fr": {
        1: "non maîtrisé",
        2: "faible",
        3: "en progression",
        4: "presque maîtrisé",
        5: "entièrement maîtrisé",
    },
}

CHECKER_PHRASES = {
    "zh": {
        "Non-empty submission": "提交内容不是空的",
        "Includes all three homework labels": "包含全部三个作业标签",
        "Enough code for review": "代码量足够批改",
        "Has at least one output line": "至少包含一行输出",
        "No obvious C++ leakage in target language": "目标语言中没有明显 C++ 写法残留",
        "Racket language line `#lang racket` or `#lang typed/racket`": "Racket 语言行 `#lang racket` 或 `#lang typed/racket`",
        "Racket prefix calls such as `(displayln value)` or `(+ a b)`": "Racket 前缀调用，例如 `(displayln value)` 或 `(+ a b)`",
        "Python output with `print(...)`": "使用 Python 的 `print(...)` 输出",
        "Python avoids C++ braces for blocks": "Python 代码块不使用 C++ 大括号",
        "Python names avoid C-style declared types": "Python 变量名不使用 C 风格类型声明",
        "C++ include for standard library support": "C++ 包含标准库头文件",
        "C++ `main` entry point": "C++ `main` 程序入口",
        "C++ output/input style such as `std::cout` or `std::cin`": "C++ 输入输出写法，例如 `std::cout` 或 `std::cin`",
        "C include for standard library support": "C 包含标准库头文件",
        "C `main` entry point": "C `main` 程序入口",
        "C I/O style such as `printf` or `scanf`": "C 输入输出写法，例如 `printf` 或 `scanf`",
        "Java class or record wrapper": "Java class 或 record 包装结构",
        "Java `main` entry point for runnable samples": "Java 可运行示例的 `main` 入口",
        "Java output with `System.out.println(...)`": "使用 Java 的 `System.out.println(...)` 输出",
        "R assignment with `<-` or clear function definitions": "使用 R 的 `<-` 赋值或清晰函数定义",
        "R output with `cat(...)` or `print(...)`": "使用 R 的 `cat(...)` 或 `print(...)` 输出",
        "R avoids C++ headers and `std::` syntax": "R 中避免 C++ 头文件和 `std::` 写法",
        "prints visible output": "打印可见输出",
        "reads or simulates input": "读取或模拟输入",
        "uses arithmetic calculation": "使用算术计算",
        "creates named values": "创建命名值",
        "uses a conditional branch": "使用条件分支",
        "uses multi-branch logic": "使用多分支逻辑",
        "checks invalid values before calculating": "计算前检查无效值",
        "uses while-style repetition": "使用 while 风格重复",
        "runs a menu or body at least once": "让菜单或主体至少运行一次",
        "uses or simulates randomness": "使用或模拟随机性",
        "uses counted or sequence repetition": "使用计数或序列重复",
        "uses nested repetition": "使用嵌套重复",
        "uses or explains a reusable function/helper": "使用或说明可复用函数/辅助函数",
        "defines a function": "定义函数",
        "calls a function and uses returned value": "调用函数并使用返回值",
        "uses a collection/list/array": "使用集合/list/array",
        "compares or uses collection types": "比较或使用集合类型",
        "declares and initializes a collection": "声明并初始化集合",
        "uses string/text operations": "使用字符串/文本操作",
        "works with characters": "处理字符",
        "defines a data type/class/struct": "定义数据类型/class/struct",
        "uses exact-case branching": "使用精确分支选择",
        "uses nested collections or grid logic": "使用嵌套集合或网格逻辑",
        "uses a vector/list-style sequence": "使用 vector/list 风格序列",
        "creates object/record values": "创建 object/record 值",
        "uses a function that calls itself": "使用会调用自身的函数",
        "searches data or uses decimals": "搜索数据或使用小数",
        "combines conditions": "组合多个条件",
        "uses nested or staged decisions": "使用嵌套或分阶段判断",
        "loops through a collection": "遍历集合",
        "uses nested loops for rows and columns": "使用嵌套循环处理行和列",
        "repeats until input is valid": "重复直到输入有效",
        "uses menu-style repeated choices": "使用菜单式重复选择",
        "creates and inspects a data frame": "创建并检查 data frame",
        "checks missing values or data types": "检查缺失值或数据类型",
        "calculates descriptive statistics": "计算描述性统计量",
        "uses grouped summaries or tables": "使用分组汇总或表格",
        "creates a statistics graph": "创建统计图",
        "uses distributions or simulation": "使用分布或模拟",
        "calculates a confidence interval": "计算置信区间",
        "runs or explains a t-test": "运行或解释 t 检验",
        "uses correlation or linear regression": "使用相关性或线性回归",
        "uses chi-square test and report wording": "使用卡方检验和报告写法",
        "Runs successfully in Judge0": "在 Judge0 中成功运行",
        "Judge0 run optional for this language": "该语言的 Judge0 运行是可选项",
        "Judge0 run available": "Judge0 运行可用",
        "Upload a file or paste code.": "请上传文件或粘贴代码。",
        "Paste or label all three programs as HW Q1, HW Q2, and HW Q3.": "请粘贴三个程序，或分别标注为 HW Q1、HW Q2 和 HW Q3。",
        "Add complete programs, not only one or two lines.": "请提交完整程序，不要只提交一两行。",
        "Print the required results so the checker can see behavior.": "请打印要求的结果，让检查器能看到程序行为。",
        "Rewrite C++ syntax using the target language's normal form.": "请用目标语言的正常写法重写 C++ 语法残留。",
        "Fix compile/runtime errors shown by Judge0 first.": "请先修复 Judge0 显示的编译或运行错误。",
        "Judge0 did not run this language.": "Judge0 没有运行这个语言。",
    },
    "ja": {
        "Non-empty submission": "提出内容が空ではない",
        "Includes all three homework labels": "3 つの宿題ラベルをすべて含む",
        "Enough code for review": "レビューに十分なコード量",
        "Has at least one output line": "少なくとも 1 行の出力がある",
        "No obvious C++ leakage in target language": "目標言語に明らかな C++ 構文が残っていない",
        "Racket language line `#lang racket` or `#lang typed/racket`": "Racket の言語行 `#lang racket` または `#lang typed/racket`",
        "Racket prefix calls such as `(displayln value)` or `(+ a b)`": "`(displayln value)` や `(+ a b)` のような Racket の前置呼び出し",
        "Python output with `print(...)`": "Python の `print(...)` による出力",
        "Python avoids C++ braces for blocks": "Python のブロックで C++ の波括弧を使っていない",
        "Python names avoid C-style declared types": "Python の名前で C 風の型宣言を使っていない",
        "C++ include for standard library support": "C++ の標準ライブラリ用 include",
        "C++ `main` entry point": "C++ の `main` エントリポイント",
        "C++ output/input style such as `std::cout` or `std::cin`": "`std::cout` や `std::cin` などの C++ 入出力",
        "C include for standard library support": "C の標準ライブラリ用 include",
        "C `main` entry point": "C の `main` エントリポイント",
        "C I/O style such as `printf` or `scanf`": "`printf` や `scanf` などの C 入出力",
        "Java class or record wrapper": "Java の class または record ラッパー",
        "Java `main` entry point for runnable samples": "実行可能な Java サンプルの `main` エントリポイント",
        "Java output with `System.out.println(...)`": "Java の `System.out.println(...)` による出力",
        "R assignment with `<-` or clear function definitions": "R の `<-` 代入または明確な関数定義",
        "R output with `cat(...)` or `print(...)`": "R の `cat(...)` または `print(...)` による出力",
        "R avoids C++ headers and `std::` syntax": "R で C++ ヘッダーや `std::` 構文を避けている",
        "prints visible output": "見える出力を表示する",
        "reads or simulates input": "入力を読む、または模擬する",
        "uses arithmetic calculation": "算術計算を使う",
        "creates named values": "名前付きの値を作る",
        "uses a conditional branch": "条件分岐を使う",
        "uses multi-branch logic": "複数分岐のロジックを使う",
        "checks invalid values before calculating": "計算前に無効な値を確認する",
        "uses while-style repetition": "while 形式の繰り返しを使う",
        "runs a menu or body at least once": "メニューまたは本体を少なくとも一度実行する",
        "uses or simulates randomness": "乱数を使う、または模擬する",
        "uses counted or sequence repetition": "カウントまたはシーケンスの繰り返しを使う",
        "uses nested repetition": "入れ子の繰り返しを使う",
        "uses or explains a reusable function/helper": "再利用できる関数/補助関数を使う、または説明する",
        "defines a function": "関数を定義する",
        "calls a function and uses returned value": "関数を呼び出し戻り値を使う",
        "uses a collection/list/array": "collection/list/array を使う",
        "compares or uses collection types": "コレクション型を比較または使用する",
        "declares and initializes a collection": "コレクションを宣言して初期化する",
        "uses string/text operations": "文字列/テキスト操作を使う",
        "works with characters": "文字を扱う",
        "defines a data type/class/struct": "データ型/class/struct を定義する",
        "uses exact-case branching": "正確なケース分岐を使う",
        "uses nested collections or grid logic": "入れ子のコレクションまたはグリッドロジックを使う",
        "uses a vector/list-style sequence": "vector/list 形式のシーケンスを使う",
        "creates object/record values": "object/record の値を作る",
        "uses a function that calls itself": "自分自身を呼び出す関数を使う",
        "searches data or uses decimals": "データ検索または小数を使う",
        "combines conditions": "条件を組み合わせる",
        "uses nested or staged decisions": "入れ子または段階的な判断を使う",
        "loops through a collection": "コレクションをループする",
        "uses nested loops for rows and columns": "行と列に入れ子ループを使う",
        "repeats until input is valid": "入力が有効になるまで繰り返す",
        "uses menu-style repeated choices": "メニュー形式の繰り返し選択を使う",
        "creates and inspects a data frame": "data frame を作成して確認する",
        "checks missing values or data types": "欠損値またはデータ型を確認する",
        "calculates descriptive statistics": "記述統計量を計算する",
        "uses grouped summaries or tables": "グループ別集計または表を使う",
        "creates a statistics graph": "統計グラフを作成する",
        "uses distributions or simulation": "分布またはシミュレーションを使う",
        "calculates a confidence interval": "信頼区間を計算する",
        "runs or explains a t-test": "t 検定を実行または説明する",
        "uses correlation or linear regression": "相関または線形回帰を使う",
        "uses chi-square test and report wording": "カイ二乗検定と報告表現を使う",
        "Runs successfully in Judge0": "Judge0 で正常に実行できる",
        "Judge0 run optional for this language": "この言語では Judge0 実行は任意",
        "Judge0 run available": "Judge0 実行が利用可能",
        "Upload a file or paste code.": "ファイルをアップロードするかコードを貼り付けてください。",
        "Paste or label all three programs as HW Q1, HW Q2, and HW Q3.": "3 つのプログラムを貼り付けるか、HW Q1、HW Q2、HW Q3 とラベル付けしてください。",
        "Add complete programs, not only one or two lines.": "1、2 行だけでなく完全なプログラムを追加してください。",
        "Print the required results so the checker can see behavior.": "チェッカーが動作を確認できるよう、必要な結果を出力してください。",
        "Rewrite C++ syntax using the target language's normal form.": "C++ 構文を目標言語の通常の形で書き直してください。",
        "Fix compile/runtime errors shown by Judge0 first.": "まず Judge0 に表示されたコンパイル/実行時エラーを修正してください。",
        "Judge0 did not run this language.": "Judge0 はこの言語を実行しませんでした。",
    },
    "ko": {
        "Non-empty submission": "제출 내용이 비어 있지 않음",
        "Includes all three homework labels": "세 개의 숙제 라벨을 모두 포함함",
        "Enough code for review": "리뷰할 만큼 충분한 코드",
        "Has at least one output line": "최소 한 줄의 출력 포함",
        "No obvious C++ leakage in target language": "목표 언어에 명백한 C++ 문법 잔여물이 없음",
        "Racket language line `#lang racket` or `#lang typed/racket`": "Racket 언어 줄 `#lang racket` 또는 `#lang typed/racket`",
        "Racket prefix calls such as `(displayln value)` or `(+ a b)`": "`(displayln value)` 또는 `(+ a b)` 같은 Racket 전위 호출",
        "Python output with `print(...)`": "Python `print(...)` 출력",
        "Python avoids C++ braces for blocks": "Python 블록에서 C++ 중괄호를 피함",
        "Python names avoid C-style declared types": "Python 이름에서 C 스타일 타입 선언을 피함",
        "C++ include for standard library support": "C++ 표준 라이브러리 include",
        "C++ `main` entry point": "C++ `main` 진입점",
        "C++ output/input style such as `std::cout` or `std::cin`": "`std::cout` 또는 `std::cin` 같은 C++ 입출력 방식",
        "C include for standard library support": "C 표준 라이브러리 include",
        "C `main` entry point": "C `main` 진입점",
        "C I/O style such as `printf` or `scanf`": "`printf` 또는 `scanf` 같은 C 입출력 방식",
        "Java class or record wrapper": "Java class 또는 record 래퍼",
        "Java `main` entry point for runnable samples": "실행 가능한 Java 샘플의 `main` 진입점",
        "Java output with `System.out.println(...)`": "Java `System.out.println(...)` 출력",
        "R assignment with `<-` or clear function definitions": "R `<-` 대입 또는 명확한 함수 정의",
        "R output with `cat(...)` or `print(...)`": "R `cat(...)` 또는 `print(...)` 출력",
        "R avoids C++ headers and `std::` syntax": "R에서 C++ 헤더와 `std::` 문법을 피함",
        "prints visible output": "보이는 출력을 출력함",
        "reads or simulates input": "입력을 읽거나 시뮬레이션함",
        "uses arithmetic calculation": "산술 계산을 사용함",
        "creates named values": "이름 붙은 값을 만듦",
        "uses a conditional branch": "조건 분기를 사용함",
        "uses multi-branch logic": "다중 분기 논리를 사용함",
        "checks invalid values before calculating": "계산 전 잘못된 값을 확인함",
        "uses while-style repetition": "while 방식 반복을 사용함",
        "runs a menu or body at least once": "메뉴 또는 본문을 최소 한 번 실행함",
        "uses or simulates randomness": "무작위성을 사용하거나 시뮬레이션함",
        "uses counted or sequence repetition": "카운트 또는 시퀀스 반복을 사용함",
        "uses nested repetition": "중첩 반복을 사용함",
        "uses or explains a reusable function/helper": "재사용 가능한 함수/헬퍼를 사용하거나 설명함",
        "defines a function": "함수를 정의함",
        "calls a function and uses returned value": "함수를 호출하고 반환값을 사용함",
        "uses a collection/list/array": "collection/list/array를 사용함",
        "compares or uses collection types": "컬렉션 타입을 비교하거나 사용함",
        "declares and initializes a collection": "컬렉션을 선언하고 초기화함",
        "uses string/text operations": "문자열/텍스트 연산을 사용함",
        "works with characters": "문자를 다룸",
        "defines a data type/class/struct": "데이터 타입/class/struct를 정의함",
        "uses exact-case branching": "정확한 case 분기를 사용함",
        "uses nested collections or grid logic": "중첩 컬렉션 또는 격자 논리를 사용함",
        "uses a vector/list-style sequence": "vector/list 스타일 시퀀스를 사용함",
        "creates object/record values": "object/record 값을 만듦",
        "uses a function that calls itself": "자기 자신을 호출하는 함수를 사용함",
        "searches data or uses decimals": "데이터를 검색하거나 소수를 사용함",
        "combines conditions": "조건을 결합함",
        "uses nested or staged decisions": "중첩 또는 단계적 판단을 사용함",
        "loops through a collection": "컬렉션을 순회함",
        "uses nested loops for rows and columns": "행과 열에 중첩 루프를 사용함",
        "repeats until input is valid": "입력이 유효할 때까지 반복함",
        "uses menu-style repeated choices": "메뉴식 반복 선택을 사용함",
        "creates and inspects a data frame": "data frame을 만들고 검사함",
        "checks missing values or data types": "결측값 또는 데이터 타입을 확인함",
        "calculates descriptive statistics": "기술 통계를 계산함",
        "uses grouped summaries or tables": "그룹별 요약 또는 표를 사용함",
        "creates a statistics graph": "통계 그래프를 만듦",
        "uses distributions or simulation": "분포 또는 시뮬레이션을 사용함",
        "calculates a confidence interval": "신뢰구간을 계산함",
        "runs or explains a t-test": "t-test를 실행하거나 설명함",
        "uses correlation or linear regression": "상관관계 또는 선형회귀를 사용함",
        "uses chi-square test and report wording": "카이제곱 검정과 보고 문구를 사용함",
        "Runs successfully in Judge0": "Judge0에서 성공적으로 실행됨",
        "Judge0 run optional for this language": "이 언어에서는 Judge0 실행이 선택 사항",
        "Judge0 run available": "Judge0 실행 가능",
        "Upload a file or paste code.": "파일을 업로드하거나 코드를 붙여넣으세요.",
        "Paste or label all three programs as HW Q1, HW Q2, and HW Q3.": "세 프로그램을 모두 붙여넣거나 HW Q1, HW Q2, HW Q3로 라벨을 붙이세요.",
        "Add complete programs, not only one or two lines.": "한두 줄이 아니라 완성된 프로그램을 추가하세요.",
        "Print the required results so the checker can see behavior.": "검사기가 동작을 볼 수 있도록 필요한 결과를 출력하세요.",
        "Rewrite C++ syntax using the target language's normal form.": "C++ 문법을 목표 언어의 일반적인 형태로 다시 작성하세요.",
        "Fix compile/runtime errors shown by Judge0 first.": "먼저 Judge0에 표시된 컴파일/런타임 오류를 고치세요.",
        "Judge0 did not run this language.": "Judge0가 이 언어를 실행하지 않았습니다.",
    },
    "fr": {
        "Non-empty submission": "Soumission non vide",
        "Includes all three homework labels": "Inclut les trois étiquettes de devoir",
        "Enough code for review": "Assez de code pour la correction",
        "Has at least one output line": "Contient au moins une ligne de sortie",
        "No obvious C++ leakage in target language": "Pas de reste évident de syntaxe C++ dans le langage cible",
        "Racket language line `#lang racket` or `#lang typed/racket`": "Ligne de langage Racket `#lang racket` ou `#lang typed/racket`",
        "Racket prefix calls such as `(displayln value)` or `(+ a b)`": "Appels préfixes Racket comme `(displayln value)` ou `(+ a b)`",
        "Python output with `print(...)`": "Sortie Python avec `print(...)`",
        "Python avoids C++ braces for blocks": "Python évite les accolades C++ pour les blocs",
        "Python names avoid C-style declared types": "Les noms Python évitent les déclarations de type façon C",
        "C++ include for standard library support": "Include C++ pour la bibliothèque standard",
        "C++ `main` entry point": "Point d'entrée C++ `main`",
        "C++ output/input style such as `std::cout` or `std::cin`": "Entrée/sortie C++ comme `std::cout` ou `std::cin`",
        "C include for standard library support": "Include C pour la bibliothèque standard",
        "C `main` entry point": "Point d'entrée C `main`",
        "C I/O style such as `printf` or `scanf`": "Entrée/sortie C comme `printf` ou `scanf`",
        "Java class or record wrapper": "Enveloppe Java class ou record",
        "Java `main` entry point for runnable samples": "Point d'entrée Java `main` pour les exemples exécutables",
        "Java output with `System.out.println(...)`": "Sortie Java avec `System.out.println(...)`",
        "R assignment with `<-` or clear function definitions": "Affectation R avec `<-` ou définitions de fonctions claires",
        "R output with `cat(...)` or `print(...)`": "Sortie R avec `cat(...)` ou `print(...)`",
        "R avoids C++ headers and `std::` syntax": "R évite les en-têtes C++ et la syntaxe `std::`",
        "prints visible output": "affiche une sortie visible",
        "reads or simulates input": "lit ou simule une entrée",
        "uses arithmetic calculation": "utilise un calcul arithmétique",
        "creates named values": "crée des valeurs nommées",
        "uses a conditional branch": "utilise une branche conditionnelle",
        "uses multi-branch logic": "utilise une logique à plusieurs branches",
        "checks invalid values before calculating": "vérifie les valeurs invalides avant le calcul",
        "uses while-style repetition": "utilise une répétition de type while",
        "runs a menu or body at least once": "exécute un menu ou un corps au moins une fois",
        "uses or simulates randomness": "utilise ou simule l'aléatoire",
        "uses counted or sequence repetition": "utilise une répétition comptée ou séquentielle",
        "uses nested repetition": "utilise une répétition imbriquée",
        "uses or explains a reusable function/helper": "utilise ou explique une fonction réutilisable",
        "defines a function": "définit une fonction",
        "calls a function and uses returned value": "appelle une fonction et utilise la valeur retournée",
        "uses a collection/list/array": "utilise une collection/liste/tableau",
        "compares or uses collection types": "compare ou utilise des types de collection",
        "declares and initializes a collection": "déclare et initialise une collection",
        "uses string/text operations": "utilise des opérations sur chaînes/texte",
        "works with characters": "travaille avec des caractères",
        "defines a data type/class/struct": "définit un type de données/class/struct",
        "uses exact-case branching": "utilise un branchement par cas précis",
        "uses nested collections or grid logic": "utilise des collections imbriquées ou une logique de grille",
        "uses a vector/list-style sequence": "utilise une séquence de type vector/list",
        "creates object/record values": "crée des valeurs object/record",
        "uses a function that calls itself": "utilise une fonction qui s'appelle elle-même",
        "searches data or uses decimals": "cherche des données ou utilise des décimales",
        "combines conditions": "combine des conditions",
        "uses nested or staged decisions": "utilise des décisions imbriquées ou par étapes",
        "loops through a collection": "parcourt une collection",
        "uses nested loops for rows and columns": "utilise des boucles imbriquées pour lignes et colonnes",
        "repeats until input is valid": "répète jusqu'à ce que l'entrée soit valide",
        "uses menu-style repeated choices": "utilise des choix répétés de type menu",
        "creates and inspects a data frame": "crée et inspecte un data frame",
        "checks missing values or data types": "vérifie les valeurs manquantes ou les types de données",
        "calculates descriptive statistics": "calcule des statistiques descriptives",
        "uses grouped summaries or tables": "utilise des résumés groupés ou des tableaux",
        "creates a statistics graph": "crée un graphique statistique",
        "uses distributions or simulation": "utilise des distributions ou une simulation",
        "calculates a confidence interval": "calcule un intervalle de confiance",
        "runs or explains a t-test": "exécute ou explique un test t",
        "uses correlation or linear regression": "utilise une corrélation ou une régression linéaire",
        "uses chi-square test and report wording": "utilise un test du khi carré et un libellé de rapport",
        "Runs successfully in Judge0": "S'exécute avec succès dans Judge0",
        "Judge0 run optional for this language": "Exécution Judge0 facultative pour ce langage",
        "Judge0 run available": "Exécution Judge0 disponible",
        "Upload a file or paste code.": "Téléversez un fichier ou collez du code.",
        "Paste or label all three programs as HW Q1, HW Q2, and HW Q3.": "Collez ou étiquetez les trois programmes HW Q1, HW Q2 et HW Q3.",
        "Add complete programs, not only one or two lines.": "Ajoutez des programmes complets, pas seulement une ou deux lignes.",
        "Print the required results so the checker can see behavior.": "Affichez les résultats demandés pour que le vérificateur voie le comportement.",
        "Rewrite C++ syntax using the target language's normal form.": "Réécrivez la syntaxe C++ avec la forme normale du langage cible.",
        "Fix compile/runtime errors shown by Judge0 first.": "Corrigez d'abord les erreurs de compilation/exécution indiquées par Judge0.",
        "Judge0 did not run this language.": "Judge0 n'a pas exécuté ce langage.",
    },
}

CHECKER_TEMPLATES = {
    "en": {
        "revise_syntax": "Revise this using normal {language} syntax.",
        "use_day_topic": "Use the Day {day} topic directly: {title}.",
    },
    "zh": {
        "revise_syntax": "请使用正常的 {language} 语法修改这一点。",
        "use_day_topic": "请直接使用第 {day} 天主题：{title}。",
    },
    "ja": {
        "revise_syntax": "通常の {language} 構文でここを修正してください。",
        "use_day_topic": "{day}日目のテーマを直接使ってください：{title}。",
    },
    "ko": {
        "revise_syntax": "정상적인 {language} 문법으로 이 부분을 수정하세요.",
        "use_day_topic": "{day}일차 주제를 직접 사용하세요: {title}.",
    },
    "fr": {
        "revise_syntax": "Révisez ceci avec la syntaxe normale de {language}.",
        "use_day_topic": "Utilisez directement le sujet du jour {day} : {title}.",
    },
}

EXECUTION_TEXT = {
    "en": {
        "judge0_code_run": "Judge0 code run",
        "not_available": "Not available.",
        "status": "Status",
        "time": "Time",
        "memory": "Memory",
        "stdout": "Stdout",
        "stderr": "Stderr",
        "compile_output": "Compile output",
        "message": "Message",
        "not_configured": "Judge0 is not configured for {target}. Public Judge0 CE currently covers Python, C, C++, Java, and R in this app.",
        "too_large": "Code was not sent to Judge0 because it is larger than 64 KB.",
        "api_error": "Judge0 could not run this code: {detail}",
        "http_error": "Judge0 returned HTTP {code}: {detail}",
        "not_saved": "Judge0 result was not saved for this older submission.",
    },
    "zh": {
        "judge0_code_run": "Judge0 代码运行",
        "not_available": "不可用。",
        "status": "状态",
        "time": "时间",
        "memory": "内存",
        "stdout": "标准输出",
        "stderr": "标准错误",
        "compile_output": "编译输出",
        "message": "消息",
        "not_configured": "Judge0 尚未配置 {target}。此应用中的公共 Judge0 CE 目前覆盖 Python、C、C++、Java 和 R。",
        "too_large": "代码超过 64 KB，未发送到 Judge0。",
        "api_error": "Judge0 无法运行这段代码：{detail}",
        "http_error": "Judge0 返回 HTTP {code}：{detail}",
        "not_saved": "这个旧提交没有保存 Judge0 结果。",
    },
    "ja": {
        "judge0_code_run": "Judge0 コード実行",
        "not_available": "利用できません。",
        "status": "状態",
        "time": "時間",
        "memory": "メモリ",
        "stdout": "標準出力",
        "stderr": "標準エラー",
        "compile_output": "コンパイル出力",
        "message": "メッセージ",
        "not_configured": "Judge0 は {target} 用に設定されていません。このアプリの公開 Judge0 CE は現在 Python、C、C++、Java、R に対応しています。",
        "too_large": "コードが 64 KB を超えるため Judge0 に送信されませんでした。",
        "api_error": "Judge0 はこのコードを実行できませんでした：{detail}",
        "http_error": "Judge0 が HTTP {code} を返しました：{detail}",
        "not_saved": "この古い提出には Judge0 結果が保存されていません。",
    },
    "ko": {
        "judge0_code_run": "Judge0 코드 실행",
        "not_available": "사용할 수 없습니다.",
        "status": "상태",
        "time": "시간",
        "memory": "메모리",
        "stdout": "표준 출력",
        "stderr": "표준 오류",
        "compile_output": "컴파일 출력",
        "message": "메시지",
        "not_configured": "Judge0가 {target}용으로 설정되어 있지 않습니다. 이 앱의 공개 Judge0 CE는 현재 Python, C, C++, Java, R을 지원합니다.",
        "too_large": "코드가 64 KB보다 커서 Judge0로 보내지 않았습니다.",
        "api_error": "Judge0가 이 코드를 실행할 수 없었습니다: {detail}",
        "http_error": "Judge0가 HTTP {code}를 반환했습니다: {detail}",
        "not_saved": "이전 제출에는 Judge0 결과가 저장되지 않았습니다.",
    },
    "fr": {
        "judge0_code_run": "Exécution du code Judge0",
        "not_available": "Non disponible.",
        "status": "Statut",
        "time": "Temps",
        "memory": "Mémoire",
        "stdout": "Sortie standard",
        "stderr": "Erreur standard",
        "compile_output": "Sortie de compilation",
        "message": "Message",
        "not_configured": "Judge0 n'est pas configuré pour {target}. Dans cette application, Judge0 CE public couvre actuellement Python, C, C++, Java et R.",
        "too_large": "Le code n'a pas été envoyé à Judge0 car il dépasse 64 KB.",
        "api_error": "Judge0 n'a pas pu exécuter ce code : {detail}",
        "http_error": "Judge0 a renvoyé HTTP {code} : {detail}",
        "not_saved": "Le résultat Judge0 n'a pas été enregistré pour cette ancienne soumission.",
    },
}

JUDGE0_STATUS_TEXT = {
    "zh": {
        "Accepted": "通过",
        "Wrong Answer": "答案错误",
        "Compilation Error": "编译错误",
        "Runtime Error (NZEC)": "运行时错误（非零退出码）",
        "Time Limit Exceeded": "超过时间限制",
    },
    "ja": {
        "Accepted": "成功",
        "Wrong Answer": "不正解",
        "Compilation Error": "コンパイルエラー",
        "Runtime Error (NZEC)": "実行時エラー（非ゼロ終了）",
        "Time Limit Exceeded": "時間制限超過",
    },
    "ko": {
        "Accepted": "통과",
        "Wrong Answer": "오답",
        "Compilation Error": "컴파일 오류",
        "Runtime Error (NZEC)": "런타임 오류(0이 아닌 종료)",
        "Time Limit Exceeded": "시간 제한 초과",
    },
    "fr": {
        "Accepted": "Accepté",
        "Wrong Answer": "Mauvaise réponse",
        "Compilation Error": "Erreur de compilation",
        "Runtime Error (NZEC)": "Erreur d'exécution (code non nul)",
        "Time Limit Exceeded": "Limite de temps dépassée",
    },
}


def translate_checker_phrase(value: str, ui_language: str) -> str:
    language = normalize_ui_language(ui_language)
    if language == "en" or not value:
        return value
    phrases = CHECKER_PHRASES.get(language, {})
    if value in phrases:
        return phrases[value]
    revise_match = re.fullmatch(r"Revise this using normal (.+) syntax\.", value)
    if revise_match:
        return CHECKER_TEMPLATES[language]["revise_syntax"].format(language=revise_match.group(1))
    topic_match = re.fullmatch(r"Use the Day (\d+) topic directly: (.+)\.", value)
    if topic_match:
        return CHECKER_TEMPLATES[language]["use_day_topic"].format(day=topic_match.group(1), title=topic_match.group(2))
    return value


def localize_code_check(report: dict | None, ui_language: str) -> dict:
    if not isinstance(report, dict):
        return {}
    language = normalize_ui_language(ui_language)
    localized = dict(report)
    rating = normalize_mastery_rating(report)
    localized["masteryRating"] = rating
    localized["masteryLabel"] = mastery_label(rating, language)
    localized["checks"] = [
        {
            **check,
            "name": translate_checker_phrase(str(check.get("name", "")), language),
            "fix": translate_checker_phrase(str(check.get("fix", "")), language),
        }
        for check in report.get("checks", [])
        if isinstance(check, dict)
    ]
    localized["strengths"] = [translate_checker_phrase(str(item), language) for item in report.get("strengths", [])]
    localized["fixes"] = [translate_checker_phrase(str(item), language) for item in report.get("fixes", [])]
    return localized


def execution_text(ui_language: str) -> dict:
    return EXECUTION_TEXT.get(normalize_ui_language(ui_language), EXECUTION_TEXT["en"])


def localized_execution_message(result: dict, ui_language: str) -> str:
    text = execution_text(ui_language)
    status = result.get("status")
    if status == "not_supported":
        return text["not_configured"].format(target=result.get("target", "this language"))
    if status == "too_large":
        return text["too_large"]
    if status == "not_saved":
        return text["not_saved"]
    if status == "api_http_error":
        return text["http_error"].format(code=result.get("httpCode", "?"), detail=result.get("errorDetail") or result.get("message") or "")
    if status == "api_error":
        return text["api_error"].format(detail=result.get("errorDetail") or result.get("message") or "")
    return result.get("message") or text["not_available"]


def localize_execution_record(result: dict | None, ui_language: str) -> dict | None:
    if not isinstance(result, dict):
        return result
    language = normalize_ui_language(ui_language)
    localized = dict(result)
    status = localized.get("status")
    localized["status"] = JUDGE0_STATUS_TEXT.get(language, {}).get(status, status)
    if not localized.get("available"):
        localized["message"] = localized_execution_message(localized, language)
    return localized


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
    if target_language == "r":
        if stripped.startswith("#"):
            return "Comment line. R ignores it when running the program."
        if "function(" in stripped:
            return "Defines a function. In R, functions are values assigned to names, often with `<-`."
        if stripped.startswith(("if ", "else if", "else")):
            return "Controls a branch. R uses parentheses for the condition and braces for the body."
        if stripped.startswith(("for ", "while ", "repeat")):
            return "Starts a loop. `repeat` runs until a `break` statement stops it."
        if "cat(" in stripped or "print(" in stripped:
            return "Prints output to the console. `cat` is usually clearer for labelled homework output."
        if "readline(" in stripped:
            return "Reads user input as text. Convert it with functions such as `as.integer` or `as.numeric` before math."
        if "<-" in stripped:
            return "Creates or updates a name. R commonly uses `<-` for assignment."
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


def local_feedback(lesson: dict, content: str, ui_language: str = "en") -> str:
    code = content.strip()
    lines = [line for line in code.splitlines() if line.strip()]
    notes: list[str] = []
    text = local_feedback_text(ui_language)

    if not code:
        return text["empty"]

    target_language = lesson.get("target_language", "racket")
    target_language_name = lesson.get("target_language_name", "Racket")
    if target_language == "racket" and "#lang racket" not in code and "#lang typed/racket" not in code:
        notes.append(text["racket_lang"])
    if target_language == "racket" and "(define" not in code and lesson["day"] >= 4:
        notes.append(text["racket_define"])
    if target_language == "racket" and "check-" not in code and lesson["day"] >= 19:
        notes.append(text["racket_tests"])
    if target_language == "python" and "def " not in code and lesson["day"] >= 4:
        notes.append(text["python_def"])
    if target_language == "c" and "#include" not in code:
        notes.append(text["c_include"])
    if target_language == "cpp" and "main(" not in code and lesson["day"] <= 12:
        notes.append(text["cpp_main"])
    if target_language == "java" and "class " not in code and "record " not in code:
        notes.append(text["java_class"])
    if target_language == "r" and not any(token in code for token in ("<-", "cat(", "print(", "function(")):
        notes.append(text["r_syntax"])
    if target_language not in {"c", "cpp"} and ("#include" in code or "std::" in code):
        notes.append(text["cpp_leak"])
    if len(lines) < 8:
        notes.append(text["short"])
    if not notes:
        notes.append(text["reasonable"])

    line_reviews = [
        f"- L{index}: `{line.strip()}` - {local_line_review(line, target_language) if normalize_ui_language(ui_language) == 'en' else text['generic_line']}"
        for index, line in enumerate(code.splitlines(), start=1)
        if line.strip()
    ][:12]
    if not line_reviews:
        line_reviews = [f"- {text['line_empty']}"]

    return (
        f"{text['title']}\n"
        f"- {text['lesson']}: {lesson['category']}\n"
        f"- {text['target_language']}: {target_language_name}\n"
        f"- {text['non_empty']}: {len(lines)}\n"
        + "\n".join(f"- {note}" for note in notes)
        + f"\n\n{text['line_review']}\n"
        + "\n".join(line_reviews)
        + f"\n\n{text['closing']}"
    )


def run_with_judge0(target: str, source_code: str, stdin: str = "") -> dict:
    language_id = judge0_language_ids().get(target)
    if not language_id:
        return {
            "available": False,
            "status": "not_supported",
            "target": target,
            "message": f"Judge0 is not configured for {target}. Public Judge0 CE currently covers Python, C, C++, Java, and R in this app.",
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
            "status": "api_http_error",
            "httpCode": error.code,
            "errorDetail": body or error.reason,
            "message": f"Judge0 returned HTTP {error.code}: {body or error.reason}",
        }
    except Exception as error:
        return {
            "available": False,
            "status": "api_error",
            "errorDetail": str(error),
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


def format_execution_result(result: dict, ui_language: str = "en") -> str:
    text = execution_text(ui_language)
    result = localize_execution_record(result, ui_language) or {}
    if not result.get("available"):
        return f"{text['judge0_code_run']}: {result.get('message', text['not_available'])}"

    lines = [
        f"{text['judge0_code_run']}:",
        f"- {text['status']}: {result.get('status', 'Unknown')}",
    ]
    if result.get("time"):
        lines.append(f"- {text['time']}: {result['time']}s")
    if result.get("memory"):
        lines.append(f"- {text['memory']}: {result['memory']} KB")
    for label, key in (
        (text["stdout"], "stdout"),
        (text["stderr"], "stderr"),
        (text["compile_output"], "compileOutput"),
        (text["message"], "message"),
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
        "r": [
            ("R assignment with `<-` or clear function definitions", "<-" in code or "function(" in code),
            ("R output with `cat(...)` or `print(...)`", "cat(" in code or "print(" in code),
            ("R avoids C++ headers and `std::` syntax", "#include" not in code and "std::" not in code),
        ],
    }
    return checks.get(target, [])


def topic_construct_checks(base_kind: str, target: str, code: str) -> list[tuple[str, bool]]:
    lower = code.lower()
    checks = {
        "output": [("prints visible output", any(token in code for token in ("display", "print(", "printf", "cout", "System.out.println", "cat(")))],
        "input": [("reads or simulates input", any(token in code for token in ("read-line", "input(", "scanf", "cin", "Scanner", "read ", "readline(", "scan(")))],
        "math": [("uses arithmetic calculation", any(token in code for token in ("+", "-", "*", "/", "%")))],
        "variable": [("creates named values", bool(re.search(r"(define\s+|=|<-)", code)))],
        "if_statement": [("uses a conditional branch", "if" in lower)],
        "else_if": [("uses multi-branch logic", any(token in lower for token in ("else", "elif", "cond", "case", "switch")))],
        "error_check": [("checks invalid values before calculating", any(token in lower for token in ("if", "error", "invalid", "cannot")))],
        "while_loop": [("uses while-style repetition", any(token in lower for token in ("while", "let loop", "loop", "repeat")))],
        "do_while": [("runs a menu or body at least once", any(token in lower for token in ("do", "while", "menu", "choice", "loop", "repeat", "break")))],
        "random_number": [("uses or simulates randomness", any(token in lower for token in ("random", "rand", "rng", "dice", "sample")))],
        "for_loop": [("uses counted or sequence repetition", any(token in lower for token in ("for", "range", "in-range")))],
        "nested_for": [("uses nested repetition", len(re.findall(r"\b(for|for\*|while)\b", lower)) >= 2 or "for*" in lower)],
        "function_intro": [("uses or explains a reusable function/helper", any(token in lower for token in ("def ", "define (", "function", "return", "helper")))],
        "create_function": [("defines a function", any(token in code for token in ("define (", "def ", "function ", "function(", "static ", "public static")))],
        "call_function": [("calls a function and uses returned value", bool(re.search(r"\w+\s*\(", code)) or bool(re.search(r"\(\w+[!?-]?\s+", code)))],
        "arrays_intro": [("uses a collection/list/array", any(token in lower for token in ("list", "vector", "array", "[", "{", "c(")))],
        "array_kinds": [("compares or uses collection types", any(token in lower for token in ("list", "vector", "array", "collection", "c(")))],
        "array_declare": [("declares and initializes a collection", any(token in lower for token in ("list", "vector", "array", "[", "{", "c(")))],
        "strings": [("uses string/text operations", any(token in lower for token in ("string", "str", "\"", "append", "length", "paste", "substr")))],
        "char_arrays": [("works with characters", any(token in lower for token in ("char", "character", "string-ref", "chars", "strsplit", "substr")))],
        "classes": [("defines a data type/class/struct", any(token in lower for token in ("class", "struct", "record", "list(")))],
        "switch_statement": [("uses exact-case branching", any(token in lower for token in ("switch", "case", "cond")))],
        "multi_arrays": [("uses nested collections or grid logic", any(token in lower for token in ("grid", "row", "column", "matrix", "list", "vector")))],
        "vectors": [("uses a vector/list-style sequence", any(token in lower for token in ("vector", "list", "array", "append", "push", "c(")))],
        "objects_classes": [("creates object/record values", any(token in lower for token in ("new ", "object", "struct", "class", "record", "list(")))],
        "recursion": [("uses a function that calls itself", (bool(re.search(r"(define\s+\((\w+)|def\s+(\w+)|\b(\w+)\s*\()", code)) and "return" in lower) or "recursive" in lower)],
        "search_float": [("searches data or uses decimals", any(token in lower for token in ("find", "search", "index", "float", "double", ".")))],
        "combined_if": [("combines conditions", any(token in lower for token in ("&&", "||", " and ", " or ", "and", "or")))],
        "nested_if": [("uses nested or staged decisions", lower.count("if") >= 2 or "cond" in lower)],
        "for_arrays": [("loops through a collection", any(token in lower for token in ("for", "map", "for/list", "foreach", "for-each")) and any(token in lower for token in ("list", "vector", "array", "[", "c(")))],
        "nested_for_multi": [("uses nested loops for rows and columns", len(re.findall(r"\b(for|for\*|while)\b", lower)) >= 2 or ("row" in lower and "col" in lower))],
        "while_validation": [("repeats until input is valid", any(token in lower for token in ("while", "loop", "valid", "invalid")))],
        "do_while_menu": [("uses menu-style repeated choices", any(token in lower for token in ("menu", "choice", "quit", "while", "do")))],
        "r_data_frame": [("creates and inspects a data frame", "data.frame" in lower and any(token in lower for token in ("nrow", "ncol", "head", "str", "summary")))],
        "r_missing_types": [("checks missing values or data types", any(token in lower for token in ("is.na", "na.omit", "colsums", "as.numeric", "as.integer", "complete.cases")))],
        "r_descriptive_stats": [("calculates descriptive statistics", any(token in lower for token in ("mean", "median", "sd", "range", "summary", "quantile")))],
        "r_grouped_summary": [("uses grouped summaries or tables", any(token in lower for token in ("aggregate", "table", "tapply", "by(")))],
        "r_graphics": [("creates a statistics graph", any(token in lower for token in ("hist", "boxplot", "plot", "abline", "png", "ggplot")))],
        "r_distribution_sim": [("uses distributions or simulation", any(token in lower for token in ("rnorm", "qnorm", "replicate", "set.seed", "sample")))],
        "r_confidence_interval": [("calculates a confidence interval", any(token in lower for token in ("qt", "standard_error", "margin", "lower", "upper", "confidence")))],
        "r_t_test": [("runs or explains a t-test", "t.test" in lower or "p-value" in lower or "paired" in lower)],
        "r_regression": [("uses correlation or linear regression", any(token in lower for token in ("lm(", "cor(", "predict", "r-squared", "summary(model")))],
        "r_chi_square_report": [("uses chi-square test and report wording", "chisq.test" in lower and any(token in lower for token in ("matrix", "table", "p-value", "report")))],
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
    add_check("Has at least one output line", any(token in code for token in ("display", "print(", "printf", "cout", "System.out.println", "cat(")), "Print the required results so the checker can see behavior.")
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
    mastery_rating = mastery_rating_from_score(score)
    fixes = [check["fix"] for check in checks if not check["passed"]][:6]
    strengths = [check["name"] for check in checks if check["passed"]][:6]
    return {
        "score": score,
        "masteryRating": mastery_rating,
        "masteryLabel": mastery_label(mastery_rating),
        "checks": checks,
        "strengths": strengths,
        "fixes": fixes,
        "programLabelsFound": labels,
        "nonEmptyLines": len(lines),
    }


def mastery_rating_from_score(score: float | int | None) -> int:
    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        numeric_score = 0.0
    if numeric_score >= 9:
        return 5
    if numeric_score >= 7:
        return 4
    if numeric_score >= 5:
        return 3
    if numeric_score >= 3:
        return 2
    return 1


def mastery_label(rating: int, ui_language: str = "en") -> str:
    labels = MASTERY_LABELS.get(normalize_ui_language(ui_language), MASTERY_LABELS["en"])
    return labels.get(max(1, min(int(rating or 1), 5)), labels[1])


def normalize_mastery_rating(report: dict | None) -> int:
    if not report:
        return 1
    rating = report.get("masteryRating")
    if isinstance(rating, (int, float)):
        return max(1, min(int(round(rating)), 5))
    return mastery_rating_from_score(report.get("score", 0))


def normalize_assignment_score(record: dict) -> float | None:
    score = record.get("assignmentScore")
    if score is None:
        score = record.get("score")
    if score is None and isinstance(record.get("codeCheck"), dict):
        score = record["codeCheck"].get("score")
    if score is None:
        return None
    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        return None
    return round(max(0.0, min(numeric_score, 10.0)), 1)


def inferred_legacy_code_check(record: dict, ui_language: str = "en") -> dict | None:
    content = str(record.get("content") or record.get("contentPreview") or "").strip()
    if not content:
        return None
    try:
        day = int(record.get("day", 0))
    except (TypeError, ValueError):
        return None
    target = normalize_target_language(record.get("target", "racket"))
    base = normalize_base_language(record.get("base", "cpp"))
    lesson = get_lesson(day, target, base, ui_language)
    if not lesson:
        return None
    execution = record.get("execution") if isinstance(record.get("execution"), dict) else None
    if not execution:
        execution = {
            "available": False,
            "status": "not_saved",
            "target": target,
            "message": (
                f"Judge0 is not configured for {target}."
                if target not in JUDGE0_DEFAULT_LANGUAGE_IDS
                else "Judge0 result was not saved for this older submission."
            ),
        }
    report = analyze_code_submission(lesson, content, execution)
    report["legacyInferred"] = True
    return report


def scored_submission(record: dict, ui_language: str = "en") -> dict:
    ui_language = normalize_ui_language(ui_language)
    cleaned = dict(record)
    code_check = cleaned.get("codeCheck") if isinstance(cleaned.get("codeCheck"), dict) else {}
    if not code_check:
        code_check = inferred_legacy_code_check(cleaned, ui_language) or {}
        if code_check:
            cleaned["codeCheck"] = code_check
    assignment_score = normalize_assignment_score(cleaned)
    mastery_rating = cleaned.get("masteryRating")
    if not isinstance(mastery_rating, (int, float)):
        mastery_rating = normalize_mastery_rating(code_check) if code_check else (
            mastery_rating_from_score(assignment_score) if assignment_score is not None else None
        )

    if assignment_score is not None:
        cleaned["assignmentScore"] = assignment_score
        cleaned["assignmentScoreMax"] = 10
        cleaned["assignmentScoreLabel"] = f"{assignment_score:g}/10"
    if mastery_rating is not None:
        cleaned["masteryRating"] = max(1, min(int(round(mastery_rating)), 5))
        cleaned["masteryLabel"] = mastery_label(cleaned["masteryRating"], ui_language)
    if isinstance(cleaned.get("execution"), dict):
        cleaned["execution"] = localize_execution_record(cleaned["execution"], ui_language)
    if code_check:
        cleaned["codeCheck"] = localize_code_check(code_check, ui_language)

    try:
        day = int(cleaned.get("day", 0))
    except (TypeError, ValueError):
        day = 0
    if day:
        target = normalize_target_language(cleaned.get("target", "racket"))
        base = normalize_base_language(cleaned.get("base", "cpp"))
        lesson = get_lesson(day, target, base, ui_language)
        if lesson:
            cleaned["targetLanguage"] = lesson.get("target_language_name", cleaned.get("targetLanguage"))
            cleaned["category"] = lesson.get("category", cleaned.get("category"))
            cleaned["title"] = lesson.get("title", cleaned.get("title"))
    return cleaned


def format_code_check_report(report: dict, ui_language: str = "en") -> str:
    text = local_feedback_text(ui_language)
    report = localize_code_check(report, ui_language)
    lines = [
        text["checker_title"],
        f"- {text['score']}: {report.get('score', 0)}/10",
        f"- {text['mastery']}: {report.get('masteryRating', 1)}/5 ({report.get('masteryLabel', mastery_label(1, ui_language))})",
        f"- {text['non_empty_lines']}: {report.get('nonEmptyLines', 0)}",
        f"- {text['labels']}: {', '.join(report.get('programLabelsFound') or []) or text['none']}",
        f"- {text['passed']}:",
    ]
    lines.extend(f"  - {item}" for item in report.get("strengths", []) or [text["none_yet"]])
    lines.append(f"- {text['fix_next']}:")
    lines.extend(f"  - {item}" for item in report.get("fixes", []) or [text["keep_improving"]])
    return "\n".join(lines)


def parse_iso_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def latest_records_by_day(records: list[dict]) -> dict[int, dict]:
    latest: dict[int, dict] = {}
    for record in records:
        try:
            day = int(record.get("day", 0))
        except (TypeError, ValueError):
            continue
        if day < 1:
            continue
        existing = latest.get(day)
        if not existing or parse_iso_datetime(record.get("createdAt")) > parse_iso_datetime(existing.get("createdAt")):
            latest[day] = record
    return latest


def build_mastery_records(records: list[dict], target: str, base: str = "cpp", ui_language: str = "en") -> list[dict]:
    ui_language = normalize_ui_language(ui_language)
    latest = latest_records_by_day(records)
    mastery_records: list[dict] = []
    for day in sorted(latest):
        record = scored_submission(latest[day], ui_language)
        lesson = get_lesson(day, target, base, ui_language)
        code_check = record.get("codeCheck") or {}
        rating = normalize_mastery_rating(code_check)
        mastery_records.append({
            "day": day,
            "title": record.get("title") or (lesson.get("title") if lesson else f"Day {day:02d}"),
            "category": record.get("category") or (lesson.get("category") if lesson else ""),
            "rating": rating,
            "label": mastery_label(rating, ui_language),
            "score": code_check.get("score"),
            "submittedAt": record.get("createdAt"),
            "target": record.get("target") or target,
        })
    return mastery_records


def build_mastery_summary(mastery_records: list[dict]) -> dict:
    if not mastery_records:
        return {
            "averageRating": None,
            "ratedLessons": 0,
            "ratings": {str(value): 0 for value in range(1, 6)},
            "weakestDay": None,
            "weakDays": [],
            "strongDays": [],
        }
    ratings = [int(item.get("rating", 1)) for item in mastery_records]
    counts = {str(value): ratings.count(value) for value in range(1, 6)}
    weak_days = sorted(
        (item for item in mastery_records if int(item.get("rating", 1)) <= 3),
        key=lambda item: (int(item.get("rating", 1)), parse_iso_datetime(item.get("submittedAt")), int(item.get("day", 0))),
    )
    weakest_day = weak_days[0] if weak_days else min(
        mastery_records,
        key=lambda item: (int(item.get("rating", 1)), parse_iso_datetime(item.get("submittedAt")), int(item.get("day", 0))),
    )
    strong_days = sorted(
        (item for item in mastery_records if int(item.get("rating", 1)) >= 4),
        key=lambda item: (-int(item.get("rating", 1)), int(item.get("day", 0))),
    )
    return {
        "averageRating": round(sum(ratings) / len(ratings), 1),
        "ratedLessons": len(ratings),
        "ratings": counts,
        "weakestDay": weakest_day,
        "weakDays": weak_days[:8],
        "strongDays": strong_days[:8],
    }


def build_pop_quiz_schedule(mastery_records: list[dict], time_zone: str = DEFAULT_TIME_ZONE) -> list[dict]:
    schedule: list[dict] = []
    now = datetime.now(timezone.utc)
    local_zone = ZoneInfo(normalize_time_zone(time_zone))
    local_now = now.astimezone(local_zone)
    for item in mastery_records:
        submitted_at = parse_iso_datetime(item.get("submittedAt"))
        if submitted_at == datetime.min.replace(tzinfo=timezone.utc):
            continue
        rating = int(item.get("rating", 1))
        for interval in POP_QUIZ_INTERVAL_DAYS:
            local_submitted_at = submitted_at.astimezone(local_zone)
            local_due_at = (local_submitted_at + timedelta(days=interval)).replace(
                hour=20,
                minute=0,
                second=0,
                microsecond=0,
            )
            due_at = local_due_at.astimezone(timezone.utc)
            if due_at < now - timedelta(days=1):
                continue
            schedule.append({
                "day": item.get("day"),
                "title": item.get("title"),
                "category": item.get("category"),
                "rating": rating,
                "label": item.get("label"),
                "score": item.get("score"),
                "submittedAt": submitted_at.isoformat(),
                "dueAt": due_at.isoformat(),
                "localDueAt": local_due_at.isoformat(),
                "date": local_due_at.date().isoformat(),
                "time": POP_QUIZ_FIXED_TIME,
                "timeZone": normalize_time_zone(time_zone),
                "intervalDays": interval,
                "due": local_due_at <= local_now,
            })
    return sorted(schedule, key=lambda item: (parse_iso_datetime(item.get("dueAt")), int(item.get("rating", 1)), int(item.get("day", 0))))[:12]


def guidance_text(ui_language: str) -> dict:
    return GUIDANCE_TEXT.get(normalize_ui_language(ui_language), GUIDANCE_TEXT["en"])


def user_learning_guidance(user: dict, profile_override: dict | None = None) -> dict:
    profile = sanitize_profile(profile_override or user.get("profile", {}))
    target = normalize_target_language(profile.get("targetLanguage", "racket"))
    base = normalize_base_language(profile.get("baseLanguage") or "cpp")
    ui_language = normalize_ui_language(profile.get("uiLanguage"))
    time_zone = normalize_time_zone(profile.get("timeZone"))
    text = guidance_text(ui_language)
    active_day = int(profile.get("activeDay", 1))
    course_length = get_course_length(target)
    active_day = max(1, min(active_day, course_length))
    lesson = get_lesson(active_day, target, base, ui_language) or get_lesson(1, target, base, ui_language)
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
    mastery_records = build_mastery_records(records, target, base, ui_language)
    mastery_summary = build_mastery_summary(mastery_records)
    weakest_day = mastery_summary.get("weakestDay")
    pop_quiz_schedule = build_pop_quiz_schedule(mastery_records, time_zone)
    next_pop_quiz = pop_quiz_schedule[0] if pop_quiz_schedule else None

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
        summary = text["no_homework"].format(target_name=target_name, day=active_day)
    else:
        score_text = text["score_text"].format(score=average_score) if average_score is not None else ""
        mastery_text = (
            text["mastery_text"].format(
                rating=mastery_summary["averageRating"],
                count=mastery_summary["ratedLessons"],
            )
            if mastery_summary.get("averageRating") is not None
            else ""
        )
        summary = text["summary"].format(
            records=len(records),
            days=len(submitted_days),
            target_name=target_name,
            score_text=score_text,
            mastery_text=mastery_text,
            done=checklist_done,
            total=checklist_total,
        )

    today = [
        text["today_1"].format(day=active_day, title=lesson["title"]),
        text["today_2"],
        text["today_3"].format(target_name=target_name),
    ]
    if missing_previous:
        today.append(text["missing_previous"].format(days=", ".join(str(day).zfill(2) for day in missing_previous)))

    habits = []
    if missing_label_count:
        habits.append(text["habit_labels"])
    if short_submission_count:
        habits.append(text["habit_short"])
    if runner_issue_count:
        habits.append(text["habit_runner"])
    if not habits:
        habits.append(text["habit_clean"])
    if checklist_total and checklist_done < checklist_total:
        habits.append(text["habit_checklist"])

    focus_areas = [
        text["focus_failed"].format(name=name, count=count)
        for name, count in common_failures
    ] or [
        text["focus_syntax"].format(target_name=target_name),
        text["focus_output"],
    ]
    if weakest_day:
        focus_areas.insert(
            0,
            text["weakest_focus"].format(
                day=int(weakest_day.get("day", 0)),
                title=weakest_day.get("title", ""),
                rating=weakest_day.get("rating", 1),
                label=weakest_day.get("label", ""),
            ),
        )
    next_steps = [
        text["next_1"],
        text["next_2"],
        text["next_3"],
        text["pop_quiz_plan"].format(time=POP_QUIZ_FIXED_TIME, curve=POP_QUIZ_MEMORY_CURVE),
    ]
    if next_pop_quiz:
        next_steps.append(
            text["pop_quiz_next"].format(
                date=next_pop_quiz.get("date"),
                time=next_pop_quiz.get("time", POP_QUIZ_FIXED_TIME),
                day=int(next_pop_quiz.get("day", 0)),
                title=next_pop_quiz.get("title", ""),
            )
        )
    for quiz in pop_quiz_schedule[:3]:
        next_steps.append(
            text["pop_quiz_due"].format(
                date=quiz.get("date"),
                time=quiz.get("time", POP_QUIZ_FIXED_TIME),
                day=int(quiz.get("day", 0)),
                interval=quiz.get("intervalDays"),
            )
        )

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
            "averageMasteryRating": mastery_summary.get("averageRating"),
            "activeDay": active_day,
            "target": target,
            "timeZone": time_zone,
        },
        "mastery": {
            "summary": mastery_summary,
            "lessons": mastery_records,
        },
        "weakestKnowledge": weakest_day,
        "popQuizSchedule": pop_quiz_schedule,
        "nextPopQuiz": next_pop_quiz,
        "popQuizPolicy": {
            "fixedTime": POP_QUIZ_FIXED_TIME,
            "intervalDays": list(POP_QUIZ_INTERVAL_DAYS),
            "memoryCurve": POP_QUIZ_MEMORY_CURVE,
            "timeZone": time_zone,
        },
    }

def build_feedback_prompt(
    lesson: dict,
    content: str,
    student_note: str,
    execution_summary: str = "",
    code_check_summary: str = "",
    ui_language: str = "en",
) -> str:
    syntax_bridge = lesson.get("syntax_bridge", {})
    docs = syntax_bridge.get("docs", lesson.get("official_docs", []))
    doc_lines = "\n".join(f"- {doc['title']}: {doc['url']}" for doc in docs)
    target_language_name = lesson.get("target_language_name", "Racket")
    base_language_name = lesson.get("base_language_name", "C++")
    target_code = syntax_bridge.get("target") or syntax_bridge.get("racket", "")
    feedback_language = guidance_text(ui_language)["feedback_language"]
    return f"""
You are a strict but friendly programming teacher. The student knows {base_language_name} and is following a {get_course_length(lesson.get('target_language'))}-day course to learn {target_language_name}.

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

Review in {feedback_language}. Use this exact structure, translated naturally into {feedback_language}:
1. Overall score out of 10 and mastery rating from 1 to 5, where 1 means not mastered and 5 means fully mastered.
2. Correctness feedback.
3. {target_language_name} style feedback, especially whether the code still follows {base_language_name} habits.
4. At least 5 concrete improvement points.
5. A recommended revised version or key revised snippet.
6. Which official documentation topic above the student should revisit.
7. Pick 3-6 important lines from the student's code and explain them line by line. For each selected line, explain important words or short phrases: keyword/function name, parentheses/braces/colon/semicolon, operators, values, variables, arguments, and result. Include the closest {base_language_name} comparison.
8. A checklist the student must complete before tomorrow's lesson.
Use the built-in code checker result as evidence. If the checker says HW labels, output, target syntax, or runner status failed, mention that directly.
Use the mastery rating to decide whether the student should repeat the lesson, do targeted practice, or move forward.
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
    ui_language: str = "en",
) -> str:
    prompt = build_feedback_prompt(lesson, content, student_note, execution_summary, code_check_summary, ui_language)
    if os.getenv("GEMINI_API_KEY", "").strip():
        try:
            return gemini_feedback(prompt)
        except Exception as error:
            return local_feedback(lesson, content, ui_language) + f"\n\nGemini AI grading failed: {error}"
    if os.getenv("OPENAI_API_KEY", "").strip():
        try:
            return openai_feedback(prompt)
        except Exception as error:
            return local_feedback(lesson, content, ui_language) + f"\n\nOpenAI grading failed: {error}"
    return local_feedback(lesson, content, ui_language)


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
        "guidance": user_learning_guidance(user),
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
    ui_language = normalize_ui_language(request.args.get("uiLanguage"))
    return jsonify({
        "languages": get_language_options(),
        "target": target,
        "base": base,
        "uiLanguage": ui_language,
        "lessons": get_lessons(target, base, ui_language),
    })


@app.get("/api/course/<int:day>")
@require_access
def lesson(day: int):
    target = normalize_target_language(request.args.get("target"))
    base = normalize_base_language(request.args.get("base"))
    ui_language = normalize_ui_language(request.args.get("uiLanguage"))
    item = get_lesson(day, target, base, ui_language)
    if not item:
        return jsonify({"error": "lesson not found"}), 404
    return jsonify(item)


@app.get("/api/submissions")
@require_access
def submissions():
    ui_language = normalize_ui_language(request.args.get("uiLanguage"))
    user = current_user()
    records = read_submissions()
    if user:
        records = [record for record in records if record.get("userId") == user["id"]]
    return jsonify({"submissions": [scored_submission(item, ui_language) for item in reversed(records)]})


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
    if request.args.get("uiLanguage"):
        profile["uiLanguage"] = normalize_ui_language(request.args.get("uiLanguage"))
    if request.args.get("timeZone"):
        profile["timeZone"] = normalize_time_zone(request.args.get("timeZone"))
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
        "day": lesson_day if lesson_day and 1 <= lesson_day <= get_course_length(target) else None,
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
    ui_language = normalize_ui_language(request.form.get("uiLanguage"))
    lesson = get_lesson(day, target, base, ui_language)
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
    execution_summary = format_execution_result(execution, ui_language)
    code_check = analyze_code_submission(lesson, content, execution)
    mastery_rating = normalize_mastery_rating(code_check)
    code_check_summary = format_code_check_report(code_check, ui_language)
    feedback = "\n\n".join([
        execution_summary,
        code_check_summary,
        ai_feedback(lesson, content, student_note, execution_summary, code_check_summary, ui_language),
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
        "assignmentScore": code_check["score"],
        "assignmentScoreMax": 10,
        "assignmentScoreLabel": f"{code_check['score']:g}/10",
        "masteryRating": mastery_rating,
        "masteryLabel": mastery_label(mastery_rating, ui_language),
        "feedback": feedback,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    records = read_submissions()
    records.append(record)
    write_submissions(records)

    return jsonify({"submission": scored_submission(record, ui_language), "sampleCode": lesson["code"]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "5000")))
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    ensure_data_files()
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=args.debug)
