#!/usr/bin/env python3
"""Create or validate a machine-readable academic project state file.

The state file is JSON so it can be edited without extra dependencies. It keeps
long paper projects from drifting across research, parsing, writing, figures,
and formatting handoffs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "paper_type",
    "language",
    "target_standard",
    "materials",
    "evidence_status",
    "draft_status",
    "figure_status",
    "format_status",
    "current_gate",
    "handoff_packets",
    "risks",
    "next_step",
]

EXPECTED_HANDOFFS = [
    "parsing_to_research",
    "research_to_writing",
    "parsing_to_writing",
    "writing_to_figures",
    "writing_to_formatting",
    "figures_to_formatting",
]

VALID_EVIDENCE_STATES = {"none", "candidate", "verified", "downloaded", "parsed", "cited", "rejected", "unresolved", "mixed"}
VALID_GATES = {
    "intake",
    "target_baseline",
    "material_inventory",
    "research_verification",
    "parsing",
    "paper_design",
    "evidence_register",
    "chapter_drafting",
    "figure_plan",
    "integrated_manuscript",
    "citation_validation",
    "formatting",
    "quality_review",
    "pre_final",
    "user_decision",
}


def template() -> dict[str, Any]:
    return {
        "paper_type": "",
        "language": "",
        "target_standard": "",
        "materials": {
            "source_pdfs": [],
            "docx_drafts": [],
            "datasets": [],
            "figures": [],
            "templates_or_guides": [],
            "target_examples": [],
        },
        "evidence_status": "candidate",
        "draft_status": "not_started",
        "figure_status": "not_started",
        "format_status": "not_started",
        "current_gate": "intake",
        "handoff_packets": {name: {"artifact": "", "status": "missing", "notes": ""} for name in EXPECTED_HANDOFFS},
        "risks": [],
        "decisions": [],
        "outputs": [],
        "next_step": "",
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("Project state must be a JSON object.")
    return payload


def validate(state: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        if field not in state:
            issues.append({"level": "error", "field": field, "issue": "missing_required_field", "action": "add field before routing work"})

    evidence_status = str(state.get("evidence_status", "")).lower()
    if evidence_status and evidence_status not in VALID_EVIDENCE_STATES:
        issues.append({"level": "warning", "field": "evidence_status", "issue": f"unexpected_state:{evidence_status}", "action": "normalize to a known evidence state"})

    current_gate = str(state.get("current_gate", "")).lower()
    if current_gate and current_gate not in VALID_GATES:
        issues.append({"level": "warning", "field": "current_gate", "issue": f"unexpected_gate:{current_gate}", "action": "map to a standard project gate"})

    handoffs = state.get("handoff_packets", {})
    if not isinstance(handoffs, dict):
        issues.append({"level": "error", "field": "handoff_packets", "issue": "not_an_object", "action": "replace with handoff packet object"})
    else:
        for handoff in EXPECTED_HANDOFFS:
            packet = handoffs.get(handoff)
            if packet is None:
                issues.append({"level": "warning", "field": f"handoff_packets.{handoff}", "issue": "missing_handoff_packet", "action": "add artifact/status/notes"})
            elif isinstance(packet, dict):
                status = str(packet.get("status", "missing")).lower()
                if status in {"ready", "complete"} and not packet.get("artifact"):
                    issues.append({"level": "error", "field": f"handoff_packets.{handoff}", "issue": "ready_without_artifact", "action": "attach artifact path or downgrade status"})

    if state.get("current_gate") in {"chapter_drafting", "integrated_manuscript"} and evidence_status not in {"verified", "parsed", "mixed"}:
        issues.append({"level": "error", "field": "evidence_status", "issue": "drafting_gate_without_verified_evidence", "action": "route to research verification or get explicit user approval"})

    if state.get("current_gate") == "formatting" and str(state.get("draft_status", "")).lower() not in {"stable", "integrated", "approved"}:
        issues.append({"level": "warning", "field": "draft_status", "issue": "formatting_before_stable_draft", "action": "confirm user accepts rework risk"})

    return issues


def write_report(path: Path, issues: list[dict[str, str]]) -> None:
    lines = ["# Project State Validation", ""]
    if not issues:
        lines.append("No blocking project-state issues detected.")
    else:
        for item in issues:
            lines.append(f"- **{item['level']}** `{item['field']}`: {item['issue']} -> {item['action']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", action="store_true", help="Write a blank project-state template")
    parser.add_argument("--state", type=Path, help="Project state JSON to validate")
    parser.add_argument("--output", type=Path, help="Template or validation report output")
    args = parser.parse_args()

    if args.init:
        if not args.output:
            raise SystemExit("--init requires --output")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(template(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"template={args.output}")
        return 0

    if not args.state:
        raise SystemExit("Provide --state or use --init --output.")
    if not args.state.exists():
        raise SystemExit(f"State file not found: {args.state}")

    state = load_json(args.state)
    issues = validate(state)
    if args.output:
        write_report(args.output, issues)
    errors = sum(1 for item in issues if item["level"] == "error")
    warnings = sum(1 for item in issues if item["level"] == "warning")
    print(f"errors={errors} warnings={warnings} issues={len(issues)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
