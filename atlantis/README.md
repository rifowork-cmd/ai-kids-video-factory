# Atlantis narration automation — first integration

This folder is separate from the existing kids-video pipeline.

## Run from GitHub Actions
1. In repository Settings → Secrets and variables → Actions, add repository secret `OPENAI_API_KEY`. Never paste the key into a source file or chat.
2. Open Actions → **Atlantis narration (manual)** → Run workflow.
3. Download the `atlantis-narration` artifact from the completed workflow run.

The workflow generates an MP3 from `atlantis/script.txt` and uploads it as a private Actions artifact. **It does not upload to YouTube, generate visuals, or charge anything until manually triggered.** OpenAI API usage is billed separately from ChatGPT subscriptions. The source script is public in this repository, so avoid adding confidential material.

Next: add timing alignment, subtitle design, licensed BGM mixing and MP4 assembly. Confirm narration quality before turning on scheduled execution.
