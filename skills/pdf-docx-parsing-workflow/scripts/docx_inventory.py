#!/usr/bin/env python3
"""Inspect a DOCX file without external dependencies.

The script reports headings, paragraph styles, captions, comments, and tracked-change
markers found in the DOCX XML package. It is intentionally conservative and does not
modify the source document.
"""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def qname(name: str) -> str:
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def text_of(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.iter(qname("w:t"))).strip()


def paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find("w:pPr/w:pStyle", NS)
    if style is None:
        return ""
    return style.attrib.get(qname("w:val"), "")


def is_caption(text: str) -> bool:
    return bool(re.match(r"^\s*(Figure|Fig\.|Table|图|表)\s*[\dA-Za-z.-]*", text))


def iter_document_paragraphs(zf: zipfile.ZipFile):
    with zf.open("word/document.xml") as handle:
        root = ET.parse(handle).getroot()
    for index, paragraph in enumerate(root.iter(qname("w:p")), start=1):
        text = text_of(paragraph)
        if not text:
            continue
        style = paragraph_style(paragraph)
        content_type = "paragraph"
        if style.lower().startswith("heading") or style.startswith("标题"):
            content_type = "heading"
        elif is_caption(text):
            content_type = "caption"
        yield {
            "part": "document",
            "location": f"p{index}",
            "content_type": content_type,
            "style": style,
            "author": "",
            "text": text,
        }


def iter_comments(zf: zipfile.ZipFile):
    if "word/comments.xml" not in zf.namelist():
        return
    with zf.open("word/comments.xml") as handle:
        root = ET.parse(handle).getroot()
    for comment in root.iter(qname("w:comment")):
        comment_id = comment.attrib.get(qname("w:id"), "")
        author = comment.attrib.get(qname("w:author"), "")
        text = text_of(comment)
        if text:
            yield {
                "part": "comments",
                "location": f"comment:{comment_id}",
                "content_type": "comment",
                "style": "",
                "author": author,
                "text": text,
            }


def iter_revisions(zf: zipfile.ZipFile):
    with zf.open("word/document.xml") as handle:
        root = ET.parse(handle).getroot()
    for tag, label in [(qname("w:ins"), "insertion"), (qname("w:del"), "deletion")]:
        for index, element in enumerate(root.iter(tag), start=1):
            text = text_of(element)
            if text:
                yield {
                    "part": "document",
                    "location": f"{label}:{index}",
                    "content_type": label,
                    "style": "",
                    "author": element.attrib.get(qname("w:author"), ""),
                    "text": text,
                }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a DOCX structure inventory CSV.")
    parser.add_argument("docx", help="Input .docx file.")
    parser.add_argument("output", help="Output CSV path.")
    args = parser.parse_args()

    docx = Path(args.docx)
    output = Path(args.output)
    if not docx.exists():
        raise SystemExit(f"DOCX not found: {docx}")

    rows = []
    with zipfile.ZipFile(docx) as zf:
        if "word/document.xml" not in zf.namelist():
            raise SystemExit(f"Not a valid DOCX package: {docx}")
        rows.extend(iter_document_paragraphs(zf))
        rows.extend(iter_comments(zf) or [])
        rows.extend(iter_revisions(zf))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["part", "location", "content_type", "style", "author", "text"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
