#!/usr/bin/env python3
"""Extract a page-level text inventory from PDFs with PyMuPDF when available."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def require_pymupdf():
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyMuPDF. Ask the user before installing it or choose another parser.") from exc
    return fitz


def quality_label(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "failed"
    if len(stripped) < 80:
        return "low"
    if "\ufffd" in stripped:
        return "low"
    return "high"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="PDF file")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV")
    parser.add_argument("--max-chars", type=int, default=1200)
    args = parser.parse_args()

    fitz = require_pymupdf()
    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    rows = []
    with fitz.open(str(args.input)) as doc:
        for index, page in enumerate(doc, start=1):
            text = page.get_text("text")
            rows.append(
                {
                    "source_path": str(args.input),
                    "source_type": "pdf",
                    "location": f"page {index}",
                    "heading": "",
                    "content_type": "page_text",
                    "text": text.strip().replace("\r", " ")[: args.max_chars],
                    "metadata": f"chars={len(text)}",
                    "quality": quality_label(text),
                    "notes": "",
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_path",
        "source_type",
        "location",
        "heading",
        "content_type",
        "text",
        "metadata",
        "quality",
        "notes",
    ]
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"pages={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
