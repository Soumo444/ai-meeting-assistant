"""
Speech-to-text transcription module.
Uses OpenAI Whisper large-v3 hosted on Groq (free tier, no credit card).
"""

import os

from openai import OpenAI

from config import GROQ_BASE, WHISPER_MODEL, MAX_AUDIO_MB


def _client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com/keys "
            "and add it to the Space secrets (or your .env file)."
        )
    return OpenAI(base_url=GROQ_BASE, api_key=api_key)


def transcribe_audio(file_path: str, language: str | None = None) -> str:
    """
    Transcribe an audio file with Whisper large-v3 on Groq.

    Args:
        file_path: Path to a local audio file (mp3/wav/m4a/flac/mp4/webm).
        language: Optional ISO-639-1 code (e.g. "en") to improve accuracy.

    Returns:
        The transcript as plain text.
    """
    if not file_path or not os.path.exists(file_path):
        raise RuntimeError("Audio file not found. Please upload a valid audio file.")

    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_AUDIO_MB:
        raise RuntimeError(
            f"Audio file is {size_mb:.1f} MB - the free tier limit is {MAX_AUDIO_MB} MB. "
            "Please split the meeting into smaller parts (or compress to mp3 64-96 kbps)."
        )

    client = _client()

    try:
        with open(file_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=f,
                response_format="text",
                temperature=0.0,
                **({"language": language} if language else {}),
            )
    except Exception as exc:  # noqa: BLE001
        message = str(exc)
        if "401" in message or "invalid_api_key" in message.lower():
            raise RuntimeError(
                "Groq rejected the API key (401). Check GROQ_API_KEY - "
                "create a new free key at https://console.groq.com/keys"
            )
        if "413" in message or "too large" in message.lower():
            raise RuntimeError(
                f"Audio too large for the free tier (limit {MAX_AUDIO_MB} MB). "
                "Split the meeting into smaller files."
            )
        if "429" in message or "rate limit" in message.lower():
            raise RuntimeError(
                "Groq free-tier rate limit reached. Wait a minute and try again."
            )
        raise RuntimeError(f"Transcription failed: {message}")

    # response_format="text" returns a plain string on most SDK versions
    text = result if isinstance(result, str) else getattr(result, "text", "")
    text = (text or "").strip()

    if not text:
        raise RuntimeError(
            "Whisper returned an empty transcript. "
            "Check that the audio contains audible speech."
        )
    return text
