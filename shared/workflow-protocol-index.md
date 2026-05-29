# Workflow Protocol Index

Use this shared index when coordinating multiple academic skills. Keep cross-skill protocol definitions here, and keep skill-local references focused on stage-specific execution.

## Shared Protocols

| protocol | read when | owner |
|---|---|---|
| Workflow mode | selecting or changing the current stage, resuming a project, or deciding the next user confirmation gate | orchestrator |
| Material passport | tracking artifacts that move across research, parsing, writing, figures, review, polishing, or formatting | orchestrator |
| Claim evidence anchor | drafting, verifying, reviewing, polishing, or captioning central claims | writing + research verification |
| Literature gap handoff | moving `LIT_GAP` items between writing and research verification | writing + research verification |
| Benchmark report | reviewing a complete draft against target papers | post-manuscript benchmark review |
| Trigger conflict matrix | deciding which skill owns an ambiguous user request | orchestrator |
| Validation policy | checking local or installed skills before use or release | repository validation script |

## Routing Rule

Use `academic-paper-orchestrator` as the only skill entrypoint that directly reads repository-level shared protocols from `../../shared/`. Other skills should keep their `SKILL.md` self-contained and align through skill-local references.

## Required Gates

Ask for user confirmation before moving past:

- inferred or unclear research field or terminology baseline;
- project design document and chapter outline;
- initial verified evidence register or gap-resolution handoff;
- benchmark set before target-readiness judgment;
- integrated draft before final polish or formatting;
- external image-generation use;
- formatting baseline before final DOCX normalization.

When a field is unclear and the user also declines to set it, default to computer science and electronic information, then mark the assumption.

## Protocol Drift Rule

If a skill-local reference disagrees with this shared layer, prefer the shared protocol for field names, handoff states, and trigger conflict decisions. Then update the local reference in the repository before relying on it again.
