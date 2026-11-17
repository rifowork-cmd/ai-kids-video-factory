# AI Kids Video Factory — development plan

## Goal
Create original Japanese and English educational videos for ages 1–6. Target running costs under JPY 30,000/month; no revenue guarantee.

## Phase 1 — draft pipeline (implemented)
- Curated safe topics: colors and numbers
- Bilingual narration and scene prompts
- Unit tests
- GitHub Actions scheduled draft generation, plus manual trigger
- Drafts retained as workflow artifacts for 14 days

## Phase 2 — media generation (not yet implemented)
- Add optional text-to-speech provider and budget controls
- Create original images with rights for commercial use
- Render video with captions, pacing, music licensing checks
- Automated checks plus human quality review

## Phase 3 — publication (not yet implemented)
- Configure YouTube OAuth safely using encrypted secrets
- Upload as private/unlisted drafts first
- Require explicit approval before public publishing
- Set made-for-kids correctly; check YouTube policies and applicable child-directed content rules

## Operating safeguards
- Never commit API keys or OAuth tokens
- No real children's faces, names, locations, or personal data
- No imitation of protected characters or unauthorized music
- Review every draft for age appropriateness, accuracy, and repetition
- Monitor API costs; stop jobs when monthly budget is reached
