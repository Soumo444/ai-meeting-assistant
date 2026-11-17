"""
AI Meeting Assistant - Configuration
=====================================
Tier 2: Strong FREE Cloud Models (Groq - free tier, no credit card)

All models are cloud-hosted. End users only need a browser.
One free Groq API key powers BOTH transcription and summarization.
"""

# -------------------------------------------------------------------
# CLOUD PROVIDER (Groq - free tier)
# -------------------------------------------------------------------
GROQ_BASE = "https://api.groq.com/openai/v1"

# Speech-to-text (free tier, 25 MB per file)
WHISPER_MODEL = "whisper-large-v3"

# -------------------------------------------------------------------
# TIER-2 STRONG FREE CLOUD MODELS (chat / summarization)
# -------------------------------------------------------------------
MODELS = {
    "openai/gpt-oss-120b": {
        "name": "GPT-OSS 120B (Groq)",
        "id": "openai/gpt-oss-120b",
        "description": "OpenAI's 120B open-weight model - top-tier reasoning, summaries and action items.",
        "context": 131072,
        "tier": "Tier 2 - Free Cloud",
        "cost": "Free (Groq free tier)",
        "speed": "Fast (~500 tok/s)",
    },
    "openai/gpt-oss-20b": {
        "name": "GPT-OSS 20B (Groq)",
        "id": "openai/gpt-oss-20b",
        "description": "OpenAI's fast 20B model - great quality at very high speed.",
        "context": 131072,
        "tier": "Tier 2 - Free Cloud",
        "cost": "Free (Groq free tier)",
        "speed": "Very fast (~1000 tok/s)",
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant (Lightning Fast)",
        "id": "llama-3.1-8b-instant",
        "description": "Ultra-fast 8B model - ideal for quick drafts and high volume.",
        "context": 131072,
        "tier": "Tier 2 - Free Cloud",
        "cost": "Free (Groq free tier)",
        "speed": "Very fast (~560 tok/s)",
    },
}

DEFAULT_MODEL = "openai/gpt-oss-120b"

# If the selected model is unavailable, try these in order
FALLBACK_ORDER = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.1-8b-instant"]

# -------------------------------------------------------------------
# SYSTEM PROMPT
# -------------------------------------------------------------------
SYSTEM_PROMPT = """You are an elite professional AI meeting assistant.

You will receive a raw meeting transcript. Produce a polished, well-structured
briefing using EXACTLY this markdown structure:

## EXECUTIVE SUMMARY
A clear 2-3 paragraph overview of what the meeting was about and the most
important outcomes. Be specific: use names, dates and numbers from the
transcript.

## KEY DECISIONS
- Bullet list of every agreement, conclusion, or decision made.
- If none were made, state "No formal decisions were recorded."

## ACTION ITEMS
1. [Owner if mentioned] Task description - Deadline (if mentioned)
2. ...
(List every concrete task. If no owner is stated, write "Unassigned".)

## TOPICS DISCUSSED
- Primary topic
- Secondary topics

## SENTIMENT & URGENCY
Overall tone (positive / neutral / tense) and urgency (low / medium / high),
with a one-sentence justification.

## RECOMMENDED FOLLOW-UPS
- Concrete next steps the team should take after this meeting.

RULES:
- Only use information present in the transcript. Never invent facts.
- Be concise but complete. No filler.
- Output valid markdown only.
"""

# Output directory for saved results
OUTPUT_DIR = "outputs"

# Temp directory for uploaded audio
TEMP_DIR = "recordings"

# Groq free-tier upload limit
MAX_AUDIO_MB = 25
