"""
Shared helpers: action-item parsing, saving outputs, formatting.
"""

import os
import re
import datetime

from config import OUTPUT_DIR, TEMP_DIR


def ensure_dirs() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def extract_action_items(summary_md: str) -> list[str]:
    """Pull the numbered/bulleted list from the '## ACTION ITEMS' section."""
    match = re.search(
        r"##\s*ACTION ITEMS\s*\n(.*?)(?=\n##\s|\Z)",
        summary_md,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return []

    items: list[str] = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^(\d+[.)]|[-*•])\s*", "", line).strip()
        if cleaned and cleaned.lower() != "none":
            items.append(cleaned)
    return items


def format_action_items(items: list[str]) -> str:
    if not items:
        return "No action items were identified in this meeting."
    return "\n".join(f"{i}. [ ] {item}" for i, item in enumerate(items, start=1))


def save_outputs(transcript: str, summary: str, model_key: str) -> dict[str, str]:
    """Persist transcript + summary to outputs/ and return the file paths."""
    ensure_dirs()
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    transcript_path = os.path.join(OUTPUT_DIR, f"transcript_{stamp}.txt")
    summary_path = os.path.join(OUTPUT_DIR, f"summary_{stamp}.md")

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    header = (
        f"# Meeting Summary\n\n"
        f"- Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"- Model: {model_key}\n\n---\n\n"
    )
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(header + summary)

    return {"transcript_path": transcript_path, "summary_path": summary_path}


def word_count(text: str) -> int:
    return len(text.split())
