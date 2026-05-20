# Code Tutor AI

A 56-day programming-learning website for students who already know C++ and want to learn Racket, Python, C, or Java through C++ comparisons.

Features:

- 56 daily course categories for each target language
- C++ syntax bridges, concise explanations, sample code, practice tasks, and daily checklists
- Browser-local checklist progress
- Homework upload or pasted-code submission
- AI homework review for correctness, style, C++ transfer habits, and next-step improvements
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
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.4-mini
ACCESS_CODE=share123
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
https://municipal-packets-ticket-believes.trycloudflare.com
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

### Real Public Deployment

Render, Railway, Fly.io, or a VPS can host this project. The repo includes:

```text
Procfile
render.yaml
```

Recommended environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.4-mini
FLASK_SECRET_KEY=a_long_random_secret
ACCESS_CODE=your_access_code
```

Set `ACCESS_CODE` on any public deployment. The site allows file uploads and AI review, so an unprotected public site can let strangers upload files or spend your API budget.

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
