#!/usr/bin/env python3
"""Audit manuscript claim anchors against an evidence register."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


ANCHOR_RE = re.compile(r"\b(CLAIM|CA|C)[-_ ]?(\d{1,4})\b|claim_anchor_id\s*[:=]\s*([A-Za-z0-9_.:-]+)", re.IGNORECASE)
SAFE_STATES = {"verified", "parsed", "writing_ready", "user_approved"}
SAFE_STRENGTHS = {"strong", "moderate", "cautious", "descriptive_only"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def normalize_anchor(raw: str) -> str:
    value = raw.strip()
    if re.fullmatch(r"\d{1,4}", value):
        return f"C{value}"
    match = re.fullmatch(r"(?:CLAIM|CA|C)[-_ ]?(\d{1,4})", value, flags=re.IGNORECASE)
    if match:
        return f"C{match.group(1)}"
    return value


def extract_anchors(text: str) -> dict[str, list[int]]:
    anchors: dict[str, list[int]] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in ANCHOR_RE.finditer(line):
            raw = match.group(3) or match.group(2) or ""
            if not raw:
                continue
            anchor = normalize_anchor(raw)
            anchors.setdefault(anchor, []).append(line_no)
    return anchors


def read_table(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload: Any = json.loads(read_text(path))
        rows = payload.get("records", payload) if isinstance(payload, dict) else payload
        if not isinstance(rows, list):
            raise SystemExit("JSON evidence register must be a list or contain records.")
        return [{str(k): str(v or "") for k, v in row.items()} for row in rows if isinstance(row, dict)]
    dialect = "excel-tab" if suffix == ".tsv" else "excel"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k): str(v or "") for k, v in row.items()} for row in csv.DictReader(handle, dialect=dialect)]


def row_anchor(row: dict[str, str]) -> str:
    for key in ("claim_anchor_id", "claim_anchor", "anchor_id", "claim_id"):
        value = row.get(key, "").strip()
        if value:
            return normalize_anchor(value)
    return ""


def row_state(row: dict[str, str]) -> str:
    for key in ("verification_state", "trust_state", "state"):
        value = row.get(key, "").strip().lower()
        if value:
            return value
    return "unknown"


def row_strength(row: dict[str, str]) -> str:
    for key in ("allowed_claim_strength", "claim_strength", "strength"):
        value = row.get(key, "").strip().lower()
        if value:
            return value
    return "unknown"


def audit(draft: Path, register: Path) -> tuple[list[dict[str, str]], dict[str, int]]:
    anchors = extract_anchors(read_text(draft))
    rows = read_table(register)
    index: dict[str, list[dict[str, str]]] = {}
    issues: list[dict[str, str]] = []

    for row in rows:
        anchor = row_anchor(row)
        if anchor:
            index.setdefault(anchor, []).append(row)

    for anchor, lines in sorted(anchors.items()):
        matched = index.get(anchor, [])
        if not matched:
            issues.append({
                "issue": "anchor_missing_from_register",
                "claim_anchor_id": anchor,
                "line": ",".join(str(x) for x in lines[:10]),
                "state": "",
                "allowed_claim_strength": "",
                "recommended_action": "add verified evidence, mark unresolved, or remove/soften claim",
            })
            continue
        if not any(row_state(row) in SAFE_STATES for row in matched):
            issues.append({
                "issue": "anchor_not_writing_ready",
                "claim_anchor_id": anchor,
                "line": ",".join(str(x) for x in lines[:10]),
                "state": ";".join(sorted({row_state(row) for row in matched})),
                "allowed_claim_strength": ";".join(sorted({row_strength(row) for row in matched})),
                "recommended_action": "route to research verification or record explicit user approval",
            })
        if not any(row_strength(row) in SAFE_STRENGTHS for row in matched):
            issues.append({
                "issue": "anchor_missing_allowed_strength",
                "claim_anchor_id": anchor,
                "line": ",".join(str(x) for x in lines[:10]),
                "state": ";".join(sorted({row_state(row) for row in matched})),
                "allowed_claim_strength": ";".join(sorted({row_strength(row) for row in matched})),
                "recommended_action": "set allowed claim strength before review, polishing, or figure caption use",
            })

    for anchor, matched in sorted(index.items()):
        if anchor not in anchors and any(row_state(row) in SAFE_STATES for row in matched):
            issues.append({
                "issue": "verified_anchor_unused_in_draft",
                "claim_anchor_id": anchor,
                "line": "",
                "state": ";".join(sorted({row_state(row) for row in matched})),
                "allowed_claim_strength": ";".join(sorted({row_strength(row) for row in matched})),
                "recommended_action": "confirm this evidence is background-only or cite/use it in the intended location",
            })

    if not anchors:
        issues.append({
            "issue": "no_claim_anchors_detected",
            "claim_anchor_id": "",
            "line": "",
            "state": "",
            "allowed_claim_strength": "",
            "recommended_action": "confirm anchor syntax or create anchors for central claims",
        })

    summary = {
        "anchors_in_draft": len(anchors),
        "anchors_in_register": len(index),
        "issues": len(issues),
        "blocking": sum(1 for item in issues if item["issue"] in {"anchor_missing_from_register", "anchor_not_writing_ready", "anchor_missing_allowed_strength"}),
    }
    return issues, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["issue", "claim_anchor_id", "line", "state", "allowed_claim_strength", "recommended_action"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]], summary: dict[str, int]) -> None:
    lines = ["# Claim Anchor Audit", "", "## Summary", ""]
    lines.extend(f"- {key}: {value}" for key, value in summary.items())
    lines.extend(["", "## Issues", ""])
    if rows:
        for row in rows:
            anchor = f" `{row['claim_anchor_id']}`" if row.get("claim_anchor_id") else ""
            line = f" line {row['line']}" if row.get("line") else ""
            lines.append(f"- **{row['issue']}**{anchor}{line}: {row['recommended_action']}")
    else:
        lines.append("No issues detected.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path, help="Markdown/plain-text manuscript draft")
    parser.add_argument("--evidence-register", required=True, type=Path, help="CSV/TSV/JSON evidence register with claim anchors")
    parser.add_argument("--output-csv", type=Path, help="Issue CSV output")
    parser.add_argument("--output-md", type=Path, help="Markdown report output")
    args = parser.parse_args()

    if not args.draft.exists():
        raise SystemExit(f"Draft not found: {args.draft}")
    if not args.evidence_register.exists():
        raise SystemExit(f"Evidence register not found: {args.evidence_register}")

    issues, summary = audit(args.draft, args.evidence_register)
    if args.output_csv:
        write_csv(args.output_csv, issues)
    if args.output_md:
        write_md(args.output_md, issues, summary)
    print(f"anchors={summary['anchors_in_draft']} register={summary['anchors_in_register']} issues={summary['issues']} blocking={summary['blocking']}")
    return 1 if summary["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
