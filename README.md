---
title: AI Meeting Assistant
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: mit
short_description: Free cloud AI meeting transcription & briefing
---

# 🤖 AI Meeting Assistant - Elite Cloud Edition

Turn any meeting recording into a professional, structured briefing in
seconds. **Completely free to use.** No Ollama, no local models, nothing to
install for end users &mdash; it runs fully in the cloud.

## 🧠 Engine (Tier 2 - strong + free)

| Task | Model | Provider |
|------|-------|----------|
| Speech-to-text | **Whisper large-v3** | Groq free tier |
| Summarization | **GPT-OSS 120B** (default) | Groq free tier |
| Alt summary models | GPT-OSS 20B, Llama 3.1 8B | Groq free tier |

One free **Groq API key** powers everything. Groq's free tier requires no
credit card.

---

## 🚀 Deploy (10 minutes)

### 1. Get a free Groq API key
1. Open <https://console.groq.com>
2. Sign up with Google/GitHub/email (free, no card)
3. Go to **API Keys** → **Create API Key** → copy `gsk_...`

### Option A - Hugging Face Spaces (recommended, free hosting)

1. Create a free account: <https://huggingface.co/join>
2. **Spaces → Create new Space**
   - Name: `ai-meeting-assistant`
   - SDK: **Gradio** · Hardware: **CPU (free)**
3. Upload every file in this folder (`app.py`, `config.py`,
   `transcription.py`, `summarizer.py`, `utils.py`, `requirements.txt`,
   `README.md`).
4. In **Settings → Variables and secrets** add a secret:
   - Name: `GROQ_API_KEY`
   - Value: your `gsk_...` key
5. The Space builds automatically. Public URL:
   `https://<your-user>-ai-meeting-assistant.hf.space`

### Option B - Run locally

```bash
cd "G:/AGENTIC STARUP"
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
set GROQ_API_KEY=gsk_xxx         # or copy .env.example to .env
python app.py                    # open http://localhost:7860
```

### Option C - Temporary public link from your PC

```bash
python launch_public.py
```
Gradio prints a public `*.gradio.live` URL you can share immediately.

---

## 🎬 How end users use it

1. Open the Space URL.
2. Upload a meeting recording (mp3 / wav / m4a / flac / mp4 / webm) — or record.
3. Pick a model (default = GPT-OSS 120B).
4. Press **🚀 Generate briefing**.
5. Read the structured output:
   - Executive summary
   - Key decisions
   - Action items (owner/deadline when mentioned)
   - Topics, sentiment & urgency
   - Recommended follow-ups
6. Download transcript `.txt` and briefing `.md`.

---

## 💰 Cost

| Component | Cost |
|-----------|------|
| HF Space hosting (CPU) | **$0** |
| Groq Whisper large-v3 | **$0** (free tier) |
| Groq Llama 3.3 70B | **$0** (free tier) || **Total** | **$0 to launch** |

Groq free-tier limits (roughly): audio up to 25 MB per file, generous daily
requests for Llama 3.3 70B. Plenty for early users; upgrade Groq's paid tier
or a Space GPU when you scale.

---

## 🩺 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `GROQ_API_KEY is not set` | Add the secret in Space settings / .env |
| 401 invalid key | Recreate the key at <https://console.groq.com/keys> |
| 429 rate limit | Free tier hourly cap — wait a minute, retry |
| 413 / too large | Split audio (limit 25 MB free tier) |
| Empty transcript | Audio has no clear speech; try cleaner recording |
| Space stalls on build | Check build logs; `requirements.txt` at repo root |

---

## 📈 Roadmap ideas

- Speaker diarization (who said what)
- Calendar / Notion / Slack integrations
- Team workspaces + meeting history
- Optional premium Tier-1 toggle (Claude 3.5 Sonnet, GPT-4o, Gemini)

---

MIT licensed. Built for the agentic AI startup — ship it. 🚀
