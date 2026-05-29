#!/usr/bin/env python3
"""Check academic figure source/export/caption package completeness."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FIGURE_RE = re.compile(r"(fig(?:ure)?)[-_ ]?(\d+[A-Za-z]?)", re.IGNORECASE)
CLAIM_RE = re.compile(r"\b(?:claim_anchor_id\s*[:=]\s*)?(C\d{1,4})\b", re.IGNORECASE)
SOURCE_EXTS = {".svg", ".drawio", ".py", ".ipynb"}
EXPORT_EXTS = {".png", ".pdf", ".tif", ".tiff", ".jpg", ".jpeg"}


def figure_id(path: Path) -> str:
    match = FIGURE_RE.search(path.stem)
    if match:
        return f"Figure_{match.group(2)}"
    return path.stem.lower()


def read_caption_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    captions: dict[str, str] = {}
    current = ""
    buffer: list[str] = []
    for line in text.splitlines():
        match = FIGURE_RE.search(line)
        if match:
            if current:
                captions[current] = "\n".join(buffer).strip()
            current = f"Figure_{match.group(2)}"
            buffer = [line]
        elif current:
            buffer.append(line)
    if current:
        captions[current] = "\n".join(buffer).strip()
    return captions


def check(package: Path, caption_file: Path | None = None) -> tuple[list[dict[str, str]], dict[str, int]]:
    files = [p for p in package.rglob("*") if p.is_file()]
    groups: dict[str, dict[str, list[Path]]] = {}
    for path in files:
        fid = figure_id(path)
        bucket = groups.setdefault(fid, {"source": [], "export": [], "caption": []})
        suffix = path.suffix.lower()
        if suffix in SOURCE_EXTS:
            bucket["source"].append(path)
        elif suffix in EXPORT_EXTS:
            bucket["export"].append(path)
        elif suffix in {".md", ".txt"} and "caption" in path.stem.lower():
            bucket["caption"].append(path)

    captions = read_caption_file(caption_file) if caption_file and caption_file.exists() else {}
    issues: list[dict[str, str]] = []

    for fid, bucket in sorted(groups.items()):
        if fid.startswith("_") or fid in {"readme", "caption", "captions"}:
            continue
        if not bucket["source"]:
            issues.append({"level": "warning", "figure_id": fid, "message": "missing editable source file"})
        if not bucket["export"]:
            issues.append({"level": "warning", "figure_id": fid, "message": "missing export preview/submission file"})
        caption_text = captions.get(fid, "")
        if not caption_text and not bucket["caption"]:
            issues.append({"level": "warning", "figure_id": fid, "message": "missing caption entry"})
        if caption_text and not CLAIM_RE.search(caption_text):
            issues.append({"level": "warning", "figure_id": fid, "message": "caption does not mention a claim anchor"})

    if not groups:
        issues.append({"level": "error", "figure_id": "", "message": "no figure files found"})

    summary = {
        "figure_groups": len(groups),
        "issues": len(issues),
        "errors": sum(1 for item in issues if item["level"] == "error"),
        "warnings": sum(1 for item in issues if item["level"] == "warning"),
    }
    return issues, summary


def write_report(path: Path, issues: list[dict[str, str]], summary: dict[str, int]) -> None:
    lines = ["# Figure Package Check", "", "## Summary", ""]
    lines.extend(f"- {key}: {value}" for key, value in summary.items())
    lines.extend(["", "## Issues", ""])
    if issues:
        for item in issues:
            fig = f" `{item['figure_id']}`" if item.get("figure_id") else ""
            lines.append(f"- **{item['level']}**{fig}: {item['message']}")
    else:
        lines.append("No issues detected.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path, help="Figure package directory")
    parser.add_argument("--captions", type=Path, help="Optional caption Markdown/TXT file")
    parser.add_argument("--output-md", type=Path, help="Markdown report output")
    args = parser.parse_args()

    if not args.package.exists() or not args.package.is_dir():
        raise SystemExit(f"Figure package directory not found: {args.package}")
    issues, summary = check(args.package, args.captions)
    if args.output_md:
        write_report(args.output_md, issues, summary)
    print(f"figure_groups={summary['figure_groups']} errors={summary['errors']} warnings={summary['warnings']}")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
