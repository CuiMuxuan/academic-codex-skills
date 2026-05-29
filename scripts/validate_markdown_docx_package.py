#!/usr/bin/env python3
"""Validate Markdown-to-DOCX package risks for formulas, citations, and cross-references."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path


INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")
BLOCK_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
CITE_RE = re.compile(r"@\w[\w:.-]*|\\cite\w*\{[^}]+\}")
CROSS_REF_RE = re.compile(r"\{#(?:fig|tbl|eq|sec):[^}]+\}|@(?:fig|tbl|eq|sec):[\w:.-]+|\\ref\{[^}]+\}|\\label\{[^}]+\}")
SUB_SUP_RE = re.compile(r"(?<!\\)[_^]\{?[\w+-]+")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def inspect_markdown(path: Path) -> list[dict[str, str]]:
    text = read_text(path)
    issues: list[dict[str, str]] = []
    inline = INLINE_MATH_RE.findall(text)
    block = BLOCK_MATH_RE.findall(text)
    cites = CITE_RE.findall(text)
    refs = CROSS_REF_RE.findall(text)
    sub_sup = SUB_SUP_RE.findall(text)

    if inline or block:
        if any("\\(" in item or "\\)" in item for item in inline):
            issues.append({"level": "warning", "area": "math", "message": "mixed dollar and LaTeX parenthesis math delimiters detected"})
    else:
        issues.append({"level": "warning", "area": "math", "message": "no Markdown/LaTeX formulas detected; confirm this is expected"})

    if sub_sup and not (inline or block):
        issues.append({"level": "warning", "area": "subscript_superscript", "message": "subscript/superscript-like markers appear outside math blocks"})
    if cites and not re.search(r"\.(bib|json|yaml|yml|ris)\b", text, flags=re.IGNORECASE):
        issues.append({"level": "warning", "area": "citations", "message": "citations detected; ensure bibliography metadata is supplied during conversion"})
    if refs and not re.search(r"\{#(?:fig|tbl|eq|sec):", text):
        issues.append({"level": "warning", "area": "cross_reference", "message": "cross-reference uses detected without obvious anchor definitions"})
    if re.search(r"TODO|LIT_GAP|needs evidence|待补证据", text, flags=re.IGNORECASE):
        issues.append({"level": "error", "area": "manuscript_readiness", "message": "unresolved evidence or TODO marker detected before DOCX finalization"})

    issues.append({"level": "info", "area": "summary", "message": f"inline_math={len(inline)} block_math={len(block)} citations={len(cites)} cross_refs={len(refs)} sub_sup_markers={len(sub_sup)}"})
    return issues


def inspect_docx(path: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not zipfile.is_zipfile(path):
        return [{"level": "error", "area": "docx", "message": "DOCX is not a valid zip package"}]
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="replace") if "word/document.xml" in names else ""
        has_math = "<m:oMath" in document_xml or "<m:oMathPara" in document_xml
        has_sup = 'w:vertAlign w:val="superscript"' in document_xml
        has_sub = 'w:vertAlign w:val="subscript"' in document_xml
        has_hyperlinks = "word/_rels/document.xml.rels" in names and "hyperlink" in archive.read("word/_rels/document.xml.rels").decode("utf-8", errors="replace")
        has_fields = "w:fldSimple" in document_xml or "w:instrText" in document_xml
    if not has_math:
        issues.append({"level": "warning", "area": "docx_math", "message": "no OMML math objects detected in DOCX"})
    if not (has_sup or has_sub):
        issues.append({"level": "warning", "area": "docx_subscript_superscript", "message": "no explicit OOXML subscript/superscript markers detected"})
    if not (has_hyperlinks or has_fields):
        issues.append({"level": "warning", "area": "docx_cross_reference", "message": "no hyperlink or field-code cross-reference signals detected"})
    issues.append({"level": "info", "area": "docx_summary", "message": f"omml_math={has_math} superscript={has_sup} subscript={has_sub} links_or_fields={has_hyperlinks or has_fields}"})
    return issues


def write_report(path: Path, issues: list[dict[str, str]]) -> None:
    lines = ["# Markdown DOCX Package Validation", ""]
    for item in issues:
        lines.append(f"- **{item['level']}** `{item['area']}`: {item['message']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", type=Path, help="Markdown source file")
    parser.add_argument("--docx", type=Path, help="DOCX output package to inspect")
    parser.add_argument("--output-md", type=Path, help="Markdown report output")
    args = parser.parse_args()

    issues: list[dict[str, str]] = []
    if not args.markdown and not args.docx:
        raise SystemExit("Provide --markdown and/or --docx.")
    if args.markdown:
        if not args.markdown.exists():
            raise SystemExit(f"Markdown not found: {args.markdown}")
        issues.extend(inspect_markdown(args.markdown))
    if args.docx:
        if not args.docx.exists():
            raise SystemExit(f"DOCX not found: {args.docx}")
        issues.extend(inspect_docx(args.docx))

    if shutil.which("pandoc") is None:
        issues.append({"level": "warning", "area": "dependency", "message": "Pandoc not found; conversion execution checks skipped"})
    else:
        issues.append({"level": "info", "area": "dependency", "message": "Pandoc is available"})

    if args.output_md:
        write_report(args.output_md, issues)
    errors = sum(1 for item in issues if item["level"] == "error")
    warnings = sum(1 for item in issues if item["level"] == "warning")
    print(f"errors={errors} warnings={warnings} issues={len(issues)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
