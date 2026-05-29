# Review Rubric And Benchmark Protocol

## Four-Criterion Review Rubric

Use this rubric to produce defensible, evidence-backed review judgments. Do not treat the four criteria as independent checkboxes: a weak evidence design can lower innovation value, and weak benchmark positioning can weaken the literature-review score.

### 1. Topic And Literature Review

Evaluate:

- frontier relevance and openness of the topic;
- theoretical value and practical significance;
- whether the literature review is comprehensive enough to set the paper’s starting score;
- whether prior work is synthesized into a problem chain rather than listed as model names;
- whether the manuscript clearly identifies the unresolved gap it addresses.

Common weaknesses:

- novelty framed only as a new model name;
- benchmark papers acknowledged but not used to define experimental requirements;
- missing recent high-quality studies;
- no distinction between task novelty, data novelty, method novelty, validation novelty, and application novelty.

Score guide:

- `5`: frontier problem, clear unresolved gap, recent and high-quality literature synthesis, benchmark set actively defines what the manuscript must prove.
- `3`: relevant topic and acceptable coverage, but the gap is broad, loosely tied to benchmark expectations, or missing recent competitors.
- `1`: topic value is asserted rather than demonstrated; literature is a list, outdated, or disconnected from the manuscript's actual contribution.

### 2. Foundational Knowledge And Research Capability

Evaluate:

- correctness of domain concepts, formulas, data processing, and method descriptions;
- scientific validity of the research design;
- data provenance and source reliability;
- whether validation avoids leakage and over-optimistic splits;
- whether claims follow from evidence;
- whether negative evidence is honestly handled.

Look for:

- clear problem decomposition;
- justified algorithms and baselines;
- ablation and stress tests;
- external or rolling validation when required;
- reproducible scripts, feature dictionaries, and command manifests.

Score guide:

- `5`: design, data provenance, baselines, validation, limitations, and reproducibility are aligned with target-level papers.
- `3`: core method is plausible, but leakage, weak baselines, incomplete statistics, or thin reproducibility remain.
- `1`: major design or evidence gaps prevent the manuscript's claims from being trusted.

### 3. Innovation And Paper Value

Evaluate:

- new insight, method, framework, dataset, protocol, or application contribution;
- whether the contribution solves an important scientific or technical problem;
- whether value is demonstrated by evidence, not only asserted;
- whether the contribution is differentiated from benchmark papers.

Classify claims as:

- promote: enough evidence for main text;
- supplement: useful but not central or not strong enough;
- reject: do not claim;
- iterate: promising but needs more evidence.

Score guide:

- `5`: contribution is clearly differentiated from benchmark papers and supported by strong evidence.
- `3`: contribution is useful but incremental, under-evidenced, or insufficiently separated from close competitors.
- `1`: novelty is cosmetic, unsupported, or not visible to likely reviewers.

### 4. Manuscript Norms And Writing Quality

Evaluate:

- academic rigor and citation discipline;
- logical structure and section-to-section continuity;
- precision and fluency of language;
- figure/table economy;
- whether the manuscript reads like a paper rather than a project log;
- whether limitations are honest and proportional.

For high-quality SCI manuscripts, prefer a compact main story with supporting details in Supplement.

Score guide:

- `5`: manuscript reads like a coherent target-journal submission; figures, tables, claims, citations, and limitations carry one focused story.
- `3`: structure and prose are serviceable, but story economy, figure logic, or citation discipline still need major revision.
- `1`: draft reads like a project report, literature list, or generated summary rather than a submission-ready manuscript.

## Benchmark Paper Selection

For detailed benchmark selection and extraction, use `benchmark-selection-and-extraction.md`. The rules below are the rubric-level scoring context.

Rank candidate benchmark papers by:

1. task similarity;
2. target variable or domain similarity;
3. method similarity;
4. validation-protocol similarity;
5. journal/source quality;
6. recency;
7. influence on likely reviewers;
8. availability of full text or reliable metadata.

Use 3-10 papers. A strong benchmark set usually includes:

- one or more closest task/method competitors;
- one or more high-level target-journal exemplars;
- one or more validation/evaluation protocol references;
- one or more domain-mechanism references if the paper has environmental, medical, social-science, or engineering mechanisms.

## Benchmark Extraction Fields

For each benchmark paper, extract when possible:

- title, authors, year, journal/source, DOI/link;
- dataset and study area;
- target variable or outcome;
- method architecture or analytical strategy;
- external inputs or covariates;
- validation protocol;
- baselines;
- metrics;
- key result;
- limitations;
- exact contrast point for the current manuscript.

## Gap Analysis Template

For each benchmark, write:

- benchmark pressure: why this paper is a serious comparator;
- current manuscript advantage;
- current manuscript gap;
- evidence required to close the gap;
- whether the gap blocks the target journal/quality tier.

Use this gap severity scale:

| Severity | Meaning |
|---|---|
| `blocking` | The target standard is not credible unless this gap is closed. |
| `major` | The manuscript can be reviewed, but acceptance/readiness is materially weakened. |
| `moderate` | The issue should be fixed in revision but does not by itself invalidate the paper. |
| `minor` | Polish, packaging, or clarity issue. |

Do not mark a benchmark gap as minor when it affects the main claim, baseline fairness, validation independence, or evidence reproducibility.

## Next-Version Plan Template

Use P0/P1/P2 priorities:

- P0: blocks target quality or creates serious overclaiming risk;
- P1: materially improves acceptance probability;
- P2: polish, packaging, and supplementary strengthening.

Each action should include:

- objective;
- exact artifact to create or revise;
- data/literature needed;
- method or experiment;
- promotion gate or acceptance criterion;
- where it goes in main paper or Supplement.

P0 actions should be few and concrete. If more than five P0 items appear, group them by root cause such as `evidence`, `benchmarking`, `claim discipline`, `figures`, or `structure`.

## Reviewer Comment Discipline

When user-provided comments are present, do not treat them as automatically correct. Each comment must be classified as accepted, partly accepted, rejected with reason, needing user decision, needing new literature, or needing new data/analysis.

Accepted and partly accepted comments must map to exact manuscript locations and revision actions. Rejected or deferred comments must include evidence-based reasons and the risk of not acting.

## Claim Triage

For each central claim, assign one state:

| State | Use |
|---|---|
| `promote` | Evidence supports the claim in the main text. |
| `soften` | Claim can remain only with narrower wording or stronger caveats. |
| `move_to_supplement` | Evidence is useful but not strong or central enough for the main story. |
| `hold_for_more_evidence` | Do not present as a conclusion yet. |
| `remove` | Claim is unsupported, misleading, or contradicted. |

This triage should be tied to manuscript section names, figure/table IDs, or benchmark-paper expectations whenever possible.

## Manual Materials Checklist

Ask the user for materials only when they cannot be inferred or retrieved:

- target journal or quality tier;
- required benchmark papers if the user has specific exemplars;
- manuscript draft if no draft is available locally;
- reference list or local PDF folder;
- data-access or sharing restrictions;
- advisor/supervisor comments;
- journal author guide or template;
- permission to search/download additional literature;
- computational budget for extra baselines or validation.

## Timing Rule

This review is a post-draft gate. It should run after the first full draft has been generated. It should not run during preliminary outline, literature search, figure making, or formatting unless the user explicitly asks to review an already-generated complete draft.
