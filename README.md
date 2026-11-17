# 🤖 AI Meeting Assistant — Elite Cloud Edition

### 🔴 **LIVE APP → [https://ai-meeting-assistant-byz2.onrender.com](https://ai-meeting-assistant-byz2.onrender.com)**

Turn any meeting recording into a professional, structured briefing in seconds.
**Completely free to use.** No installation, no local models — it runs fully in
the cloud.

> ⏱️ The app is hosted on Render's free tier, so it sleeps after ~15 minutes of
> inactivity. The first visit may take 30–60 seconds to wake up — just wait and
> the page loads.

---

## 🧠 Engine (Tier 2 — strong + free)

| Task | Model | Provider |
|------|-------|----------|
| Speech-to-text | **Whisper large-v3** | Groq free tier |
| Summarization | **GPT-OSS 120B** (default) | Groq free tier |
| Alt summary models | GPT-OSS 20B, Llama 3.1 8B | Groq free tier |

One free **Groq API key** powers everything. Groq's free tier requires no
credit card.

---

## 🎬 How to use it

1. Open the live app: <https://ai-meeting-assistant-byz2.onrender.com>
2. Upload a meeting recording (mp3 / wav / m4a / flac / mp4 / webm) — or record.
3. Pick a model (default = GPT-OSS 120B, the strongest free option).
4. Press **🚀 Generate briefing**.
5. Read the structured output:
   - Executive summary
   - Key decisions
   - Action items (owner/deadline when mentioned)
   - Topics, sentiment & urgency
   - Recommended follow-ups
6. Download the transcript `.txt` and briefing `.md`.

---

## 🚀 Run it yourself

### 1. Get a free Groq API key
1. Open <https://console.groq.com>
2. Sign up with Google/GitHub/email (free, no card)
3. Go to **API Keys** → **Create API Key** → copy `gsk_...`

### 2. Run locally

```bash
git clone https://github.com/Soumo444/ai-meeting-assistant.git
cd ai-meeting-assistant
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
set GROQ_API_KEY=gsk_xxx         # or copy .env.example to .env
python app.py                    # open http://localhost:7860
```

### 3. Deploy your own copy (free)

This repo ships with [`render.yaml`](render.yaml), so Render can deploy it in
one click:

1. Create a free account at <https://render.com>
2. **New → Web Service** → connect this repo
3. Add environment variable `GROQ_API_KEY` = your `gsk_...` key
4. Deploy — Render gives you a public `https://...onrender.com` URL

---

## 💰 Cost

| Component | Cost |
|-----------|------|
| Render hosting (free tier) | **$0** |
| Groq Whisper large-v3 | **$0** (free tier) |
| Groq GPT-OSS 120B | **$0** (free tier) |
| **Total** | **$0 to launch** |

Groq free-tier limits (roughly): audio up to 25 MB per file (~15–20 min of
mp3) and generous daily chat requests. Plenty for early users; upgrade Groq's
paid tier or hosting when you scale.

---

## 🩺 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Page takes ~60s to load | Free-tier cold start — wait, then refresh |
| `GROQ_API_KEY is not set` | Add the key in Render environment settings |
| 401 invalid key | Recreate the key at <https://console.groq.com/keys> |
| 429 rate limit | Free tier hourly cap — wait a minute, retry |
| 413 / too large | Split audio (limit 25 MB free tier) |
| Empty transcript | Audio has no clear speech; try cleaner recording |

---

## 📈 Roadmap ideas

- Speaker diarization (who said what)
- Calendar / Notion / Slack integrations
- Team workspaces + meeting history
- Optional premium Tier-1 toggle (Claude, GPT-4o, Gemini)

---

MIT licensed. Built for the agentic AI startup — ship it. 🚀
