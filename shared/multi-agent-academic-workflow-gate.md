# Multi-Agent Academic Workflow Gate

Use this shared protocol when coordinating academic paper, thesis, dissertation, review-paper, reviewer-response, or manuscript-quality workflows that can benefit from parallel review, verification, QA, or action-plan decomposition.

This protocol makes multi-agent planning the default for substantial paper workflows. It does not make sub-agents the final decision maker, and it does not allow unconfirmed edits.

## Default Rule

For substantial academic workflows, first decide whether the task has independent review or verification slices that can be checked in parallel. If yes, propose a multi-agent check plan before execution.

Before actually starting sub-agents, state:

- which checks will run in parallel;
- each sub-agent's scope;
- allowed inputs and materials;
- expected output table or checklist;
- what the main agent will do after results return;
- whether any external directory or network access may be needed.

Wait for user confirmation before starting sub-agents, unless the user has already given full permission, automatic-execution permission, or an equivalent instruction that clearly allows sub-agent execution without further confirmation.

## Environment Capability Rule

Actual sub-agent use depends on the current runtime and tool policy.

- If sub-agent tools are available and user confirmation or prior full permission exists, use them for suitable parallel checks.
- If sub-agent tools are unavailable, blocked, or disallowed by the current environment, run the same checks serially and state the limitation.
- Do not silently drop a planned parallel check because the tool is unavailable.

## When To Use Sub-Agents

Use sub-agents for bounded, independent, review-like or verification-like tasks with clear inputs and outputs:

| task slice | suitable sub-agent work | owner workflow |
|---|---|---|
| Literature and evidence verification | DOI/title checks, citation authenticity, evidence-to-claim support checks, reference download or material request lists | research verification + writing |
| Complete manuscript review | structure logic, method support, experiment support, contribution clarity, benchmark gap checks, claim risk triage | post-manuscript benchmark review |
| Sentence-level language review | section-by-section or subsection-by-subsection strict checks for abstract wording, undefined terms, operation-record residue, sentence purpose, citation distance, bilingual strength drift | writing + post-draft review |
| Figure and formatting QA | figure text readability, Draw.io source-path checks, formula/superscript/subscript conversion risk, DOCX/PDF conversion risk, citation cross-reference risk | figures + formatting |
| Reviewer-comment action planning | classify comments, identify accepted/partial/rejected/deferred items, extract material blockers, draft candidate action rows | writing + post-draft review |

Use the main agent locally for the immediate blocking task when the next step depends on it.

## When Not To Use Sub-Agents

Do not start sub-agents for:

- one short sentence, one title, one citation, one small wording question, or another simple local task;
- a task where the main agent can answer directly with lower overhead;
- final claim arbitration;
- final contribution framing;
- final wording integration;
- final rebuttal position;
- user-confirmation decisions;
- write operations, file deletion, full manuscript rewriting, figure redraw, format conversion, Git commits, pushes, releases, global installation, or other state-changing operations.

For simple local tasks, the main agent may skip sub-agents and briefly state the reason if relevant.

## Access And Search Rule

Sub-agents may read the materials assigned to their scope and the references needed to complete the assigned check.

If a sub-agent needs an external directory or network search to complete its check, it may proceed when the task scope makes that access relevant and the current environment permits it. If the path, privacy boundary, source scope, or permission state is unclear, the agent must ask the user instead of silently skipping, guessing, or downgrading the check.

Do not let a sub-agent expand into unrelated external directories, unrelated papers, unrelated projects, or unrelated web searches.

## Sub-Agent Output Format

Each sub-agent should return a structured result that the main agent can merge:

```text
subagent_report:
- scope:
- materials_checked:
- method:
- findings:
  - id:
    location:
    finding:
    evidence_or_locator:
    risk: P0/P1/P2/P3
    recommended_action:
    blocked_items:
- conflicts_or_uncertainties:
- no_issue_items:
- suggested_handoff:
```

For reviewer-comment plans, use:

```text
comment_action_slice:
- comment_id:
- stance: accept/partly_accept/reject/defer/material_blocked
- rationale:
- concrete_revision_action:
- affected_location:
- required_material:
- risk:
```

For strict language review, include every assigned sentence, including acceptable sentences.

## Main-Agent Merge Rule

The main agent must merge sub-agent outputs before any user-facing decision:

1. Deduplicate repeated findings.
2. Normalize locations, evidence locators, risk levels, and action wording.
3. Separate confirmed findings from uncertain findings.
4. Identify conflicts between sub-agent conclusions.
5. Tie each recommended action to a specific manuscript location, evidence item, figure/table, reviewer comment, or material request.
6. Produce a single user-facing synthesis, not separate unmerged sub-agent reports.

When sub-agent conclusions conflict, list:

- conflict topic;
- conflicting conclusions;
- evidence or locator behind each conclusion;
- main-agent interpretation;
- recommended resolution;
- what user confirmation is needed.

Wait for user confirmation before moving from conflicted review results into rewriting, deletion, figure redraw, formatting conversion, or reviewer-response finalization.

## Confirmation Gates

Ask for user confirmation before:

- starting sub-agents, unless prior full or automatic-execution permission exists;
- expanding strict sentence-by-sentence review beyond the user-specified chapter, subsection, paragraph, or sentence;
- resolving conflicts among sub-agent conclusions;
- turning sub-agent findings into manuscript rewriting;
- deleting, moving, or substantially rewriting manuscript content;
- redrawing figures or changing Draw.io source files;
- performing lossy conversion of formulas, superscripts/subscripts, citations, cross-references, figures, or tables;
- writing files, committing, pushing, releasing, installing globally, or changing external project state.

## Main-Agent Ownership

Sub-agents may provide findings, risks, material requests, and recommended actions. The main agent remains responsible for:

- final scope control;
- final evidence interpretation;
- final manuscript-quality judgment;
- final user-facing plan;
- final writing style integration;
- final decision on what to ask the user;
- all state-changing operations after user confirmation.

Sub-agents must not:

- make final acceptance/rejection decisions for reviewer comments;
- decide final contribution framing;
- silently expand scope;
- rewrite unassigned sections;
- modify manuscript files;
- delete content;
- redraw figures;
- convert formats;
- commit, push, release, or install.

## Minimal Planning Template

Use this compact plan before launching sub-agents:

```text
multi_agent_plan:
- reason:
- subagents:
  - name:
    scope:
    materials:
    output:
    external_access_needed: yes/no
- main_agent_local_work:
- confirmation_needed: yes/no
```

If the user has already authorized automatic execution, set `confirmation_needed: no` and state the authorization source.
