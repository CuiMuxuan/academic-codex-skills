#!/usr/bin/env python3
"""Audit rough citation/bibliography consistency in plain-text drafts.

This is a lightweight first pass. It does not verify source identity. It finds
simple author-year citations and compares them with bibliography-like entries.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

YEAR_RE = r"(?:19|20)\d{2}[a-z]?"
INBODY_RE = re.compile(r"\b([A-Z][A-Za-z'’-]+)\s*(?:et al\.)?,?\s*\(?(" + YEAR_RE + r")\)?")
BIB_RE = re.compile(r"^\s*([A-Z][A-Za-z'’-]+).*?\b(" + YEAR_RE + r")\b", re.MULTILINE)


def normalize(author: str, year: str) -> str:
    return f"{author.lower()}-{year.lower()}"


def collect_inbody(text: str) -> set[str]:
    return {normalize(author, year) for author, year in INBODY_RE.findall(text)}


def collect_bib(text: str) -> set[str]:
    return {normalize(author, year) for author, year in BIB_RE.findall(text)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path, help="Plain-text or Markdown draft")
    parser.add_argument("--bibliography", type=Path, help="Optional bibliography text; defaults to draft")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    args = parser.parse_args()

    draft_text = args.draft.read_text(encoding="utf-8-sig", errors="replace")
    bib_text = (
        args.bibliography.read_text(encoding="utf-8-sig", errors="replace")
        if args.bibliography
        else draft_text
    )

    inbody = collect_inbody(draft_text)
    bib = collect_bib(bib_text)
    rows = []
    for key in sorted(inbody - bib):
        rows.append({"issue": "in_body_missing_bibliography", "key": key})
    for key in sorted(bib - inbody):
        rows.append({"issue": "bibliography_not_cited", "key": key})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["issue", "key"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"in_body={len(inbody)} bibliography={len(bib)} issues={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
