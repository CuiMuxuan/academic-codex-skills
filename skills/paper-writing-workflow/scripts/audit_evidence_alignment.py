#!/usr/bin/env python3
"""Audit draft citations against an evidence register.

The script is intentionally conservative. It checks whether citation keys used
in Markdown/Pandoc or LaTeX-style citations exist in the evidence register and
whether their trust state is acceptable for writing. It also reports unresolved
`needs evidence` markers and verified register items that are not cited.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


PANDOC_CITE_RE = re.compile(r"@([A-Za-z0-9_:.#/$%&+?<>~|-]+)")
LATEX_CITE_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
NEEDS_EVIDENCE_RE = re.compile(
    r"(needs\s+evidence|need\s+evidence|evidence\s+needed|TODO\s*:?\s*evidence|待补证据|需要证据|需补充证据)",
    re.IGNORECASE,
)

VERIFIED_STATES = {"verified", "parsed", "downloaded", "cited", "user_approved"}
UNSAFE_STATES = {"candidate", "unresolved", "rejected", "mismatch", "unknown", ""}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def extract_citations(text: str) -> set[str]:
    keys = set(PANDOC_CITE_RE.findall(text))
    for group in LATEX_CITE_RE.findall(text):
        for key in group.split(","):
            cleaned = key.strip()
            if cleaned:
                keys.add(cleaned)
    return keys


def line_markers(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if NEEDS_EVIDENCE_RE.search(line):
            rows.append(
                {
                    "issue": "needs_evidence_marker",
                    "citation_key": "",
                    "state": "",
                    "line": str(line_no),
                    "detail": line.strip()[:240],
                    "recommended_action": "resolve claim support or keep explicit evidence gap",
                }
            )
    return rows


def read_register(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(read_text(path))
        rows = payload.get("records", payload) if isinstance(payload, dict) else payload
        return [{str(k): str(v) for k, v in row.items()} for row in rows]
    dialect = "excel-tab" if suffix == ".tsv" else "excel"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k): str(v or "") for k, v in row.items()} for row in csv.DictReader(handle, dialect=dialect)]


def key_for_row(row: dict[str, str]) -> str:
    for field in ("citation_key", "id", "source_id", "evidence_id", "key"):
        value = row.get(field, "").strip()
        if value:
            return value
    return ""


def state_for_row(row: dict[str, str]) -> str:
    for field in ("trust_state", "verification_state", "state"):
        value = row.get(field, "").strip().lower()
        if value:
            return value
    return "unknown"


def row_title(row: dict[str, str]) -> str:
    for field in ("title", "claim_or_finding", "intended_use", "notes"):
        value = row.get(field, "").strip()
        if value:
            return value
    return ""


def build_register_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        key = key_for_row(row)
        if key and key not in index:
            index[key] = row
    return index


def audit(draft_text: str, register_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    citations = extract_citations(draft_text)
    index = build_register_index(register_rows)
    issues = line_markers(draft_text)

    for key in sorted(citations):
        row = index.get(key)
        if row is None:
            issues.append(
                {
                    "issue": "citation_missing_from_register",
                    "citation_key": key,
                    "state": "",
                    "line": "",
                    "detail": "citation key used in draft but not found in register",
                    "recommended_action": "verify source or remove citation before final draft",
                }
            )
            continue
        state = state_for_row(row)
        if state not in VERIFIED_STATES:
            issues.append(
                {
                    "issue": "citation_not_writing_ready",
                    "citation_key": key,
                    "state": state,
                    "line": "",
                    "detail": row_title(row)[:240],
                    "recommended_action": "route to academic-research-verification or ask user to approve provisional use",
                }
            )

    for key, row in sorted(index.items()):
        state = state_for_row(row)
        intended_use = row.get("intended_use", "") or row.get("target_chapter", "")
        if state in VERIFIED_STATES and key not in citations and intended_use:
            issues.append(
                {
                    "issue": "verified_register_item_unused",
                    "citation_key": key,
                    "state": state,
                    "line": "",
                    "detail": row_title(row)[:240],
                    "recommended_action": "cite where relevant or keep as background-only evidence",
                }
            )

    if not citations:
        issues.append(
            {
                "issue": "no_citations_detected",
                "citation_key": "",
                "state": "",
                "line": "",
                "detail": "no Pandoc @key or LaTeX citation keys found",
                "recommended_action": "confirm citation style or provide draft with citation keys",
            }
        )

    summary = {
        "citations_detected": len(citations),
        "register_records": len(register_rows),
        "issues": len(issues),
        "missing_from_register": sum(1 for item in issues if item["issue"] == "citation_missing_from_register"),
        "not_writing_ready": sum(1 for item in issues if item["issue"] == "citation_not_writing_ready"),
        "needs_evidence_markers": sum(1 for item in issues if item["issue"] == "needs_evidence_marker"),
    }
    return issues, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["issue", "citation_key", "state", "line", "detail", "recommended_action"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summary: dict[str, Any], issues: list[dict[str, str]]) -> None:
    lines = [
        "# Evidence Alignment Audit",
        "",
        "## Summary",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in summary.items())
    lines.extend(["", "## Issues", ""])
    if issues:
        for item in issues:
            citation = f" `{item['citation_key']}`" if item.get("citation_key") else ""
            line = f" line {item['line']}" if item.get("line") else ""
            lines.append(f"- **{item['issue']}**{citation}{line}: {item['recommended_action']}")
    else:
        lines.append("No issues detected by the deterministic audit.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path, help="Markdown/plain-text/LaTeX draft")
    parser.add_argument("--evidence-register", required=True, type=Path, help="CSV/TSV/JSON evidence register")
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    if not args.draft.exists():
        raise SystemExit(f"Draft not found: {args.draft}")
    if not args.evidence_register.exists():
        raise SystemExit(f"Evidence register not found: {args.evidence_register}")

    draft_text = read_text(args.draft)
    register_rows = read_register(args.evidence_register)
    issues, summary = audit(draft_text, register_rows)
    write_csv(args.output_csv, issues)
    if args.output_md:
        write_markdown(args.output_md, summary, issues)
    print(f"citations={summary['citations_detected']} register={summary['register_records']} issues={summary['issues']} output={args.output_csv}")
    return 1 if summary["missing_from_register"] or summary["not_writing_ready"] else 0


if __name__ == "__main__":
    sys.exit(main())
