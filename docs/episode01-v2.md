# Episode 01 V2 — safe preview pipeline

This branch adds an **opt-in** GitHub Actions workflow (manual dispatch only). It does **not** upload to YouTube, generate new factual footage, or spend API credits.

1. Supply a licensed 115+ second source file at `assets/episode01/source.mp4` (large video files are better stored outside Git; adjust the workflow to download a secure artifact).
2. Run the **Episode 01 V2 preview and QC** workflow manually.
3. Download the output video and `qc_report.json` artifact.
4. Perform the human review listed in the QC report before any publication.

The current renderer is a **recut prototype** using eight titled scenes, different crops and no audio. It is not a final narrated episode. Next phase: distinct scene assets, licensed BGM, narration alignment, subtitle timing, and evidence/rights review.

Note: The previous repository may target children's videos; do not automatically publish the mystery episode to a children's channel without reviewing audience and channel strategy.
