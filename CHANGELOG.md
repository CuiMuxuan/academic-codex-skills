# Changelog

All notable changes to this project will be documented here.

## Unreleased

### Added

- Claude Code support (dual-target, Codex remains primary):
  - `install-claude.ps1` (Windows) and `install-claude.sh` (macOS/Linux) install the
    same skills into `~/.claude/skills` and `~/.claude/shared`, mirroring `install.ps1`.
  - `scripts/validate_skills.py` gains `--target {codex,claude}`; under `claude` the
    Codex-only `quick_validate.py` absence is reported as info instead of a warning,
    so `--strict` passes.
  - README section "在 Claude Code 中使用(双端共存)" with install and trigger guidance.
- Revision-control architecture update:
  - Added `language-style-review` for non-writing academic language, wording, grammar,
    AI-like phrasing, translation, figure/table text, and citation-sentence review.
  - Added `revision-control` for sentence-level revision rounds, object libraries,
    pass/fail confirmations, latest sentence-review drafts, project standards,
    material dependency records, and upgrade plans.
  - Added shared schemas for revision-control contracts, language-style review reports,
    project review standards, manuscript objects, and revision upgrade plans.
  - Updated writing, benchmark review, de-AI polishing, and orchestrator boundaries so
    language diagnosis, post-draft quality review, sentence-level state management, and
    final polishing are owned by separate skills.

### Notes

- Codex and Claude Code targets share one source tree; Claude Code support remains
  metadata-compatible with the updated skill set.
- `agents/openai.yaml` is Codex-only metadata and is harmlessly ignored by Claude Code.

## v0.1.0 - 2026-05-18

Initial public release.

### Added

- Academic Codex skills bundle with 8 focused skills:
  - `academic-paper-orchestrator`
  - `academic-research-verification`
  - `pdf-docx-parsing-workflow`
  - `paper-writing-workflow`
  - `academic-figure-workflow`
  - `academic-de-ai-polishing`
  - `academic-formatting-workflow`
  - `post-manuscript-benchmark-review`
- Windows installation script: `install.ps1`.
- Example prompts in `examples/prompts.md`.
- Project README with install instructions, recommended workflow, quality principles, and repository layout.
- MIT License.

### Notes

- This release focuses on local Codex skill installation by copying the `skills/` folders into `.codex/skills`.
- Some bundled utilities may require optional Python packages depending on the task and local environment.
