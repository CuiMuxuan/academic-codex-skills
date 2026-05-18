# Academic Codex Skills

An opinionated bundle of high-quality Codex skills for academic papers, theses, and manuscripts.

## Included Skills

- `academic-paper-orchestrator`
- `academic-research-verification`
- `pdf-docx-parsing-workflow`
- `paper-writing-workflow`
- `academic-figure-workflow`
- `academic-de-ai-polishing`
- `academic-formatting-workflow`
- `post-manuscript-benchmark-review`

## What This Repo Is For

Use this repo as a portable skill pack for:

- thesis and dissertation workflows;
- literature verification and evidence registers;
- chapter drafting and revision;
- figure planning and publication-ready diagram workflows;
- benchmark review after a first full draft;
- de-AI polishing with argument discipline;
- formatting and Word/DOCX normalization.

## Install

Copy the `skills/` subdirectories into your Codex skills folder:

- Windows: `C:\Users\<you>\.codex\skills`
- macOS/Linux: `~/.codex/skills`

Example:

```powershell
Copy-Item -Recurse -Force .\skills\* $env:USERPROFILE\.codex\skills
```

## Recommended Entry Point

Start with:

- `$academic-paper-orchestrator` for full projects;
- `$paper-writing-workflow` for drafting and revision;
- `$post-manuscript-benchmark-review` after a complete first draft.

## Notes

- Skills are optimized for academic writing and evidence-driven workflows.
- The repository is designed to be copied locally; it does not require a package manager.
