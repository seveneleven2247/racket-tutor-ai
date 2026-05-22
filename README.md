# CodeBridge

A 56-day programming-learning website that uses one known language as a bridge to teach C++, C, Java, Python, and Racket.

Features:

- 56 daily course categories for each target language
- C++ syntax bridges, concise explanations, sample code, practice tasks, and daily checklists
- Browser-local checklist progress
- Homework upload or pasted-code submission
- Built-in Judge0 code execution for Python, C, C++, and Java submissions
- Built-in static code checker that verifies labels, target-language syntax, visible output, topic usage, and runner status
- AI homework review for correctness, style, C++ transfer habits, and next-step improvements
- Day-by-day guidance based on each user's submissions, checker scores, checklist progress, and repeated habits
- Phrase-level syntax breakdowns for sample-code lines
- Local rule-based feedback when `OPENAI_API_KEY` is not configured

## Run Locally

```bash
cd ~/Public/racket-tutor-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py --port 5055
```

Open:

```text
http://127.0.0.1:5055
```

## Configure AI Review

Edit `.env`:

```bash
GEMINI_API_KEY=your_google_ai_studio_api_key
GEMINI_MODEL=gemini-2.5-flash
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.4-mini
ACCESS_CODE=share123
```

Set at least one of `GEMINI_API_KEY` or `OPENAI_API_KEY`. If neither is configured, CodeBridge still gives local line-by-line feedback for short submissions, but deeper paragraph-level AI review is disabled.

## Configure Judge0 Code Runner

CodeBridge can send submitted code to Judge0 before AI review. The run result is saved with the submission and shown in review history.

Default public endpoint:

```bash
JUDGE0_API_URL=https://ce.judge0.com
```

Default language IDs used by this app:

```text
Python: 109
C: 103
C++: 105
Java: 91
```

Public Judge0 CE does not currently provide Racket in this app's language list. Racket submissions still receive AI/local feedback. If you self-host a Judge0 image that supports Racket, set:

```bash
JUDGE0_RACKET_LANGUAGE_ID=your_racket_language_id
```

For a different Judge0 deployment, override multiple IDs:

```bash
JUDGE0_LANGUAGE_IDS={"python":109,"c":103,"cpp":105,"java":91,"racket":999}
```

Restart the Flask app after changing `.env`:

```bash
python app.py --port 5055
```

Do not commit `.env`; it is intentionally ignored by git.

## Public Sharing

### Temporary Tunnel

For a temporary public URL, run:

```bash
cloudflared tunnel --url http://127.0.0.1:5055
```

The currently shared tunnel URL is:

```text
https://possess-flu-treasure-lopez.trycloudflare.com
```

Current access code:

```text
share123
```

This URL only works while both the local Flask app and the `cloudflared` process are running.

### Local Network Sharing

```bash
python app.py --host 0.0.0.0 --port 5055
```

Then open this from another device on the same Wi-Fi:

```text
http://your-computer-lan-ip:5055
```

### Permanent Public Deployment

The `trycloudflare.com` URL is temporary. It stops working when your computer sleeps, disconnects, restarts, or the local tunnel process stops.

Use Render, Railway, Fly.io, or a VPS for a permanent public URL. The repo includes:

```text
Procfile
render.yaml
```

Render setup:

1. Push this repo to GitHub.
2. In Render, choose **New +** → **Blueprint**.
3. Connect `https://github.com/seveneleven2247/racket-tutor-ai`.
4. Render will read `render.yaml`, create a web service, and mount a persistent disk at `/var/data`.
5. Add real AI keys in Render environment variables if you want AI grading.

Recommended environment variables:

```bash
DATA_DIR=/var/data
GEMINI_API_KEY=your_google_ai_studio_key
GEMINI_MODEL=gemini-2.5-flash
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.4-mini
FLASK_SECRET_KEY=a_long_random_secret
ACCESS_CODE=your_access_code
```

Set `ACCESS_CODE` on any public deployment. The site allows file uploads and AI review, so an unprotected public site can let strangers upload files or spend your API budget.

Render's persistent disk is important. Without it, `users.json`, `submissions.json`, and uploaded homework files can disappear on redeploy.

## Project Files

```text
app.py              Flask backend
course_data.py      56-day course generator
static/index.html   Main frontend page
static/styles.css   Styles
static/app.js       Frontend behavior
data/uploads/       Uploaded homework files
data/submissions.json generated submission records
```
