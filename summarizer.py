"""
Meeting summarization module.
Uses Tier-2 strong FREE cloud models on Groq (free tier, no credit card).
"""

import os

from openai import OpenAI

from config import (
    MODELS,
    DEFAULT_MODEL,
    FALLBACK_ORDER,
    GROQ_BASE,
    SYSTEM_PROMPT,
)


def _client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com/keys "
            "and add it to the Space secrets (or your .env file)."
        )
    return OpenAI(base_url=GROQ_BASE, api_key=api_key)


def _truncate_for_model(transcript: str, model_key: str) -> str:
    """Keep the transcript inside ~80% of the model's context window."""
    ctx_tokens = MODELS.get(model_key, MODELS[DEFAULT_MODEL])["context"]
    max_chars = int(ctx_tokens * 0.8 * 3.5)  # rough chars-per-token estimate
    if len(transcript) > max_chars:
        return transcript[:max_chars] + "\n\n[...transcript truncated for processing...]"
    return transcript


def _call_model(model_key: str, transcript: str) -> str:
    model = MODELS[model_key]
    client = _client()

    response = client.chat.completions.create(
        model=model["id"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Here is the raw meeting transcript. "
                    "Produce the briefing in the exact format requested.\n\n"
                    f"--- TRANSCRIPT START ---\n{_truncate_for_model(transcript, model_key)}\n"
                    "--- TRANSCRIPT END ---"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    content = (response.choices[0].message.content or "").strip()
    if not content:
        raise RuntimeError("The model returned an empty summary.")
    return content


def summarize_meeting(transcript: str, model_key: str = DEFAULT_MODEL) -> tuple[str, str]:
    """
    Summarize a meeting transcript.

    Returns:
        (summary_markdown, model_actually_used)

    If the selected model fails, automatically falls back through
    FALLBACK_ORDER so end users always get a result.
    """
    if not transcript or not transcript.strip():
        raise RuntimeError("Transcript is empty - nothing to summarize.")

    if model_key not in MODELS:
        model_key = DEFAULT_MODEL

    order = [model_key] + [m for m in FALLBACK_ORDER if m != model_key]

    errors: list[str] = []
    for key in order:
        try:
            return _call_model(key, transcript), key
        except Exception as exc:  # noqa: BLE001 - report and try next model
            errors.append(f"{MODELS[key]['name']}: {exc}")

    raise RuntimeError(
        "All cloud models failed:\n- " + "\n- ".join(errors)
    )
