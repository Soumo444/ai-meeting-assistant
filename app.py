"""
AI Meeting Assistant - Elite Cloud Edition
==========================================
Tier-2 strong FREE cloud models (Hugging Face Inference API).

Run locally:      python app.py
Deploy to cloud:  Hugging Face Spaces (Gradio) - no installs for end users.
"""

import os
import traceback

import gradio as gr

from config import MODELS, DEFAULT_MODEL, OUTPUT_DIR, TEMP_DIR
from transcription import transcribe_audio
from summarizer import summarize_meeting
from utils import (
    ensure_dirs,
    extract_action_items,
    format_action_items,
    save_outputs,
    word_count,
)

ensure_dirs()

MODEL_CHOICES = [(m["name"], key) for key, m in MODELS.items()]
DEFAULT_LABEL = MODELS[DEFAULT_MODEL]["name"]


def _model_info_md(model_key: str) -> str:
    m = MODELS.get(model_key, MODELS[DEFAULT_MODEL])
    return (
        f"### {m['name']}\n"
        f"**Tier:** {m['tier']} | **Cost:** {m['cost']} | "
        f"**Speed:** {m['speed']} | **Context:** {m['context']:,} tokens\n\n"
        f"{m['description']}"
    )


def process_meeting(audio_path, model_key, progress=gr.Progress()):
    """Full pipeline: upload -> Whisper -> Tier-2 LLM -> structured briefing."""
    if not audio_path:
        return (
            "Please upload an audio file first.",
            "",
            "",
            "⚠️ No audio uploaded.",
            None,
            None,
        )

    model_key = model_key or DEFAULT_MODEL
    model_label = MODELS[model_key]["name"]

    try:
        # Step 1 - transcription
        progress(0.1, desc="Uploading audio to Whisper...")
        progress(0.3, desc="Transcribing with Whisper large-v3...")
        transcript = transcribe_audio(audio_path)
        progress(0.55, desc=f"Transcription done ({word_count(transcript)} words)")

        # Step 2 - summarization
        progress(0.65, desc=f"Summarizing with {model_label}...")
        summary, used_key = summarize_meeting(transcript, model_key)
        used_label = MODELS[used_key]["name"]
        progress(0.9, desc="Extracting action items...")

        # Step 3 - action items
        actions = extract_action_items(summary)
        actions_md = format_action_items(actions)

        # Step 4 - save files (works locally; on HF Spaces outputs/ is ephemeral)
        files = save_outputs(transcript, summary, used_label)

        note = "" if used_key == model_key else (
            f"\n\n> ⚠️ *{model_label} was unavailable - "
            f"used fallback model: **{used_label}**.*"
        )
        status = (
            f"✅ **Done!** Transcribed {word_count(transcript)} words | "
            f"Summary by **{used_label}** | {len(actions)} action item(s) found."
            f"{note}"
        )

        progress(1.0, desc="Complete")
        return (
            transcript,
            summary,
            actions_md,
            status,
            files["transcript_path"],
            files["summary_path"],
        )

    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        message = (
            "### ❌ Processing failed\n\n"
            f"**Reason:** {exc}\n\n"
            "**What to try:**\n"
            "- Make sure the audio contains clear speech (mp3 / wav / m4a).\n"
            "- For long meetings, split the file into 10-15 minute parts.\n"
            "- If the free-tier rate limit is hit (HTTP 429), wait a minute and retry.\n"
            "- Check that `GROQ_API_KEY` is set in Space settings."
        )
        return ("", message, "", "❌ Error - see summary tab for details.", None, None)


def reset_all():
    return (
        None,
        "",
        "",
        "",
        "✅ Ready - upload an audio file to begin.",
        None,
        None,
        _model_info_md(DEFAULT_MODEL),
        None,
    )


CSS = """
.gradio-container { font-family: 'Inter', 'Segoe UI', sans-serif; max-width: 1200px !important; margin: auto; }
.app-header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 28px; border-radius: 14px; color: #fff; margin-bottom: 18px; }
.app-header h1 { margin: 0 0 6px 0; font-size: 30px; color: #ffffff !important; }
.app-header p { margin: 0; color: #e6ecff !important; opacity: .9; }
.badge { display: inline-block; background: #00b894; color: #fff; border-radius: 999px;
  padding: 3px 12px; font-size: 12px; font-weight: 600; margin-right: 6px; }
footer { visibility: hidden; }
"""

with gr.Blocks(
    title="AI Meeting Assistant - Elite Cloud Edition",
    theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
    css=CSS,
) as demo:

    gr.HTML(
        """
        <div class="app-header">
          <h1>🤖 AI Meeting Assistant</h1>
          <p>Professional meeting transcription &amp; intelligence &mdash; powered by strong free cloud models</p>
          <div style="margin-top:12px">
            <span class="badge">Whisper large-v3</span>
            <span class="badge">Tier-2 Free Cloud LLMs</span>
            <span class="badge">No installation required</span>
          </div>
        </div>
        """
    )

    status = gr.Markdown(
        "✅ **Ready** - upload an audio file to begin.",
    )

    with gr.Row():
        # ---------------- LEFT: input ----------------
        with gr.Column(scale=5):
            with gr.Group():
                audio_in = gr.Audio(
                    label="📁 Meeting audio (mp3 / wav / m4a / flac)",
                    type="filepath",
                    sources=["upload", "microphone"],
                )

                model_dd = gr.Dropdown(
                    choices=MODEL_CHOICES,
                    value=DEFAULT_MODEL,
                    label="🧠 AI model (Tier-2 free cloud)",
                    interactive=True,
                )
                model_card = gr.Markdown(_model_info_md(DEFAULT_MODEL))

            with gr.Row():
                run_btn = gr.Button("🚀 Generate briefing", variant="primary", scale=3)
                reset_btn = gr.Button("🗑 Reset", scale=1)

            gr.Markdown(
                "**Tips**\n"
                "- Clear audio, minimal background noise\n"
                "- Free tier accepts files up to 25 MB (~15-20 min of mp3)\n"
                "- Longer meetings: split into parts and process each one"
            )

        # ---------------- RIGHT: output ----------------
        with gr.Column(scale=7):
            with gr.Tabs():
                with gr.TabItem("🧾 Executive briefing"):
                    summary_out = gr.Markdown(
                        "*Your structured meeting briefing will appear here.*"
                    )
                with gr.TabItem("📝 Transcript"):
                    transcript_out = gr.Textbox(
                        label="Full transcript",
                        lines=18,
                        show_copy_button=True,
                    )
                with gr.TabItem("✅ Action items"):
                    actions_out = gr.Markdown(
                        "*Extracted action items will appear here.*"
                    )
                with gr.TabItem("💾 Downloads"):
                    transcript_file = gr.File(label="Transcript (.txt)")
                    summary_file = gr.File(label="Briefing (.md)")

    gr.Markdown(
        "---\n"
        "**Tier-2 free cloud models** &mdash; completely free to use via the "
        "Groq API (free tier). No Ollama, no local models, nothing for "
        "end users to install."
    )

    # ---------------- wiring ----------------
    model_dd.change(_model_info_md, inputs=model_dd, outputs=model_card)

    run_btn.click(
        fn=process_meeting,
        inputs=[audio_in, model_dd],
        outputs=[
            transcript_out,
            summary_out,
            actions_out,
            status,
            transcript_file,
            summary_file,
        ],
    )

    reset_btn.click(
        fn=reset_all,
        inputs=None,
        outputs=[
            audio_in,
            transcript_out,
            summary_out,
            actions_out,
            status,
            transcript_file,
            summary_file,
            model_card,
            model_dd,
        ],
    )


if __name__ == "__main__":
    demo.queue(default_concurrency_limit=4, max_size=20)
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", "7860"))),
        share=False,
        show_error=True,
    )
