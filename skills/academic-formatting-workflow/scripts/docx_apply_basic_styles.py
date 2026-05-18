#!/usr/bin/env python3
"""Apply a conservative DOCX baseline with python-docx.

This script is intentionally narrow. It normalizes common body and heading
styles, saves a new copy, and does not update Word-only fields such as TOC.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def require_python_docx():
    try:
        import docx  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: python-docx. Ask the user before installing it.") from exc
    return docx


def set_font(style, name: str, size_pt: float | None = None):
    from docx.shared import Pt  # type: ignore

    style.font.name = name
    if size_pt:
        style.font.size = Pt(size_pt)


def apply_baseline(document, body_font: str, heading_font: str):
    from docx.enum.text import WD_LINE_SPACING  # type: ignore
    from docx.shared import Pt  # type: ignore

    styles = document.styles
    if "Normal" in styles:
        set_font(styles["Normal"], body_font, 12)
        styles["Normal"].paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        styles["Normal"].paragraph_format.first_line_indent = Pt(24)
    for name, size in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12)):
        if name in styles:
            set_font(styles[name], heading_font, size)
            styles[name].paragraph_format.first_line_indent = None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--body-font", default="Times New Roman")
    parser.add_argument("--heading-font", default="Arial")
    args = parser.parse_args()

    docx = require_python_docx()
    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    document = docx.Document(str(args.input))
    apply_baseline(document, args.body_font, args.heading_font)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(args.output))
    print(f"saved={args.output}")
    print("manual_check=Open in Word to refresh TOC, fields, page numbers, and cross-references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
