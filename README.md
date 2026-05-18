# Academic Codex Skills

High-quality Codex skills for academic papers, theses, dissertations, literature verification, manuscript writing, academic figures, DOCX formatting, and post-draft benchmark review.

This repository packages an end-to-end academic writing workflow as portable Codex skills. It is designed for researchers, graduate students, supervisors, and technical writers who want AI assistance without losing evidence discipline, citation traceability, or manuscript-quality gates.

## Why This Exists

Generic AI writing help often drifts into smooth but unsupported academic prose. This skill pack is built around a stricter workflow:

1. Verify sources before using them.
2. Parse PDFs and DOCX files into reusable structured evidence.
3. Draft only from verified or explicitly approved evidence.
4. Design figures from claims, data, and source facts.
5. Polish prose without changing claim boundaries.
6. Format only after content is stable.
7. Review the full draft against real benchmark papers before final revision.

## Included Skills

| Skill | Use For |
|---|---|
| `academic-paper-orchestrator` | Coordinate the full thesis or paper workflow and route work to focused skills. |
| `academic-research-verification` | Verify DOI/title matches, bibliography quality, citation authenticity, and evidence registers. |
| `pdf-docx-parsing-workflow` | Parse PDFs, DOCX drafts, comments, tracked changes, formatting templates, and evidence notes. |
| `paper-writing-workflow` | Plan, draft, revise, and integrate academic sections from verified evidence and benchmark writing patterns. |
| `academic-figure-workflow` | Plan and create academic figures, mechanism diagrams, draw.io diagrams, and Nature-style multi-panel plots. |
| `academic-de-ai-polishing` | Reduce mechanical AI-like academic prose while preserving evidence, citations, and technical scope. |
| `academic-formatting-workflow` | Normalize DOCX formatting against school handbooks, templates, or journal guides. |
| `post-manuscript-benchmark-review` | Review a complete first draft against 3-10 benchmark papers and produce a next-version plan. |

## Install

Clone the repository:

```powershell
git clone https://github.com/CuiMuxuan/academic-codex-skills.git
cd academic-codex-skills
```

Install on Windows:

```powershell
.\install.ps1
```

Or copy manually:

```powershell
Copy-Item -Recurse -Force .\skills\* $env:USERPROFILE\.codex\skills
```

On macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Restart Codex after installation so the skills are discovered.

## Recommended Workflow

For a full paper or thesis project, start with:

```text
Use $academic-paper-orchestrator to plan an end-to-end workflow for my thesis/paper.
```

Typical sequence:

1. `$academic-paper-orchestrator`
2. `$academic-research-verification`
3. `$pdf-docx-parsing-workflow`
4. `$paper-writing-workflow`
5. `$academic-figure-workflow`
6. `$academic-de-ai-polishing`
7. `$post-manuscript-benchmark-review`
8. `$academic-formatting-workflow`

The order is flexible, but source verification and evidence preparation should happen before serious drafting.

## Example Prompts

Full project:

```text
Use $academic-paper-orchestrator to plan an end-to-end workflow for my master's thesis. I have a topic, 25 PDFs, an old DOCX draft with supervisor comments, and a school formatting guide.
```

Literature verification:

```text
Use $academic-research-verification to verify this bibliography, check DOI/title matches, and create an evidence register for chapter drafting.
```

Benchmark-calibrated writing:

```text
Use $paper-writing-workflow to draft an Introduction subsection after I provide five benchmark papers from the target journal and a verified evidence register.
```

Figure planning:

```text
Use $academic-figure-workflow to design a Nature-grade multi-panel figure from my panel claims and source data.
```

Post-draft review:

```text
Use $post-manuscript-benchmark-review to evaluate my complete first manuscript draft against 3-10 benchmark papers and give a P0/P1/P2 next-version plan.
```

More examples are in [examples/prompts.md](examples/prompts.md).

## Quality Principles

- Do not fabricate papers, DOIs, results, figures, or claims.
- Treat verified evidence as the source of truth.
- Ask for missing materials when quality would materially improve.
- Keep target-paper and benchmark comparisons evidence-based.
- Separate drafting, polishing, formatting, and post-draft review.
- Preserve user data boundaries and local files.

## Repository Layout

```text
academic-codex-skills/
  README.md
  CHANGELOG.md
  LICENSE
  install.ps1
  examples/
    prompts.md
  skills/
    academic-paper-orchestrator/
    academic-research-verification/
    pdf-docx-parsing-workflow/
    paper-writing-workflow/
    academic-figure-workflow/
    academic-de-ai-polishing/
    academic-formatting-workflow/
    post-manuscript-benchmark-review/
```

## Version

Current release: `v0.1.0`

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## License

MIT License. See [LICENSE](LICENSE).
