#!/usr/bin/env python3
"""Create a DOCX style and structure inventory without external dependencies."""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def qn(name: str) -> str:
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def attr(element, name: str) -> str:
    return element.attrib.get(qn(name), "") if element is not None else ""


def read_xml(package: zipfile.ZipFile, name: str):
    try:
        return ET.fromstring(package.read(name))
    except KeyError:
        return None


def collect_styles(package: zipfile.ZipFile) -> list[dict]:
    root = read_xml(package, "word/styles.xml")
    if root is None:
        return []
    rows = []
    for style in root.findall("w:style", NS):
        name = style.find("w:name", NS)
        based_on = style.find("w:basedOn", NS)
        rows.append(
            {
                "record_type": "style",
                "id": attr(style, "w:styleId"),
                "name": attr(name, "w:val"),
                "style_type": attr(style, "w:type"),
                "based_on": attr(based_on, "w:val"),
                "outline_level": "",
                "paragraph_count": "",
                "notes": "",
            }
        )
    return rows


def collect_paragraph_styles(package: zipfile.ZipFile) -> list[dict]:
    root = read_xml(package, "word/document.xml")
    if root is None:
        return []
    counts: dict[str, int] = {}
    for paragraph in root.findall(".//w:p", NS):
        style = paragraph.find("w:pPr/w:pStyle", NS)
        style_id = attr(style, "w:val") or "(default)"
        counts[style_id] = counts.get(style_id, 0) + 1
    return [
        {
            "record_type": "paragraph_style_usage",
            "id": style_id,
            "name": "",
            "style_type": "paragraph",
            "based_on": "",
            "outline_level": "",
            "paragraph_count": count,
            "notes": "",
        }
        for style_id, count in sorted(counts.items())
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    rows: list[dict] = []
    with zipfile.ZipFile(args.input) as package:
        rows.extend(collect_styles(package))
        rows.extend(collect_paragraph_styles(package))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "record_type",
        "id",
        "name",
        "style_type",
        "based_on",
        "outline_level",
        "paragraph_count",
        "notes",
    ]
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"records={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
