#!/usr/bin/env python3
"""Extract PDF page text, tables, and OCR recovery notes into structured files.

Requires PyMuPDF. Uses PyMuPDF table extraction when available and falls back to
pdfplumber for tables if installed. OCR is opt-in through --ocr auto|always and
uses PyMuPDF's OCR bridge when the local Tesseract setup supports it.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def require_pymupdf():
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyMuPDF. Ask the user before installing it.") from exc
    return fitz


def optional_pdfplumber():
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        return None
    return pdfplumber


def quality_label(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "failed"
    if len(stripped) < 80 or "\ufffd" in stripped:
        return "low"
    return "high"


def clean_text(text: str, max_chars: int) -> str:
    return text.strip().replace("\r", " ")[:max_chars]


def ocr_text(page, lang: str, tessdata: str | None) -> tuple[str, str]:
    kwargs: dict[str, Any] = {"language": lang, "full": True}
    if tessdata:
        kwargs["tessdata"] = tessdata
    try:
        textpage = page.get_textpage_ocr(**kwargs)
    except TypeError:
        kwargs.pop("tessdata", None)
        textpage = page.get_textpage_ocr(**kwargs)
    except Exception as exc:
        return "", f"ocr_failed:{exc}"
    try:
        return page.get_text("text", textpage=textpage), "ocr_applied"
    except Exception as exc:
        return "", f"ocr_text_extract_failed:{exc}"


def extract_pymupdf_tables(page, page_number: int) -> tuple[list[dict[str, Any]], str]:
    if not hasattr(page, "find_tables"):
        return [], "pymupdf_find_tables_unavailable"
    try:
        table_finder = page.find_tables()
    except Exception as exc:
        return [], f"pymupdf_table_failed:{exc}"
    tables = getattr(table_finder, "tables", []) or []
    rows: list[dict[str, Any]] = []
    for table_index, table in enumerate(tables, start=1):
        try:
            extracted = table.extract()
        except Exception as exc:
            rows.append(
                {
                    "page": page_number,
                    "table_id": f"p{page_number}_t{table_index}",
                    "row": "",
                    "column": "",
                    "text": "",
                    "method": "pymupdf",
                    "quality": "failed",
                    "notes": f"extract_failed:{exc}",
                }
            )
            continue
        for row_index, row in enumerate(extracted or [], start=1):
            for col_index, cell in enumerate(row or [], start=1):
                rows.append(
                    {
                        "page": page_number,
                        "table_id": f"p{page_number}_t{table_index}",
                        "row": row_index,
                        "column": col_index,
                        "text": str(cell or "").strip(),
                        "method": "pymupdf",
                        "quality": "medium",
                        "notes": "",
                    }
                )
    return rows, "ok" if rows else "no_tables_found"


def extract_pdfplumber_tables(pdf_path: Path) -> list[dict[str, Any]]:
    pdfplumber = optional_pdfplumber()
    if pdfplumber is None:
        return []
    rows: list[dict[str, Any]] = []
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                for table_index, table in enumerate(page.extract_tables() or [], start=1):
                    for row_index, row in enumerate(table or [], start=1):
                        for col_index, cell in enumerate(row or [], start=1):
                            rows.append(
                                {
                                    "page": page_number,
                                    "table_id": f"p{page_number}_plumber_t{table_index}",
                                    "row": row_index,
                                    "column": col_index,
                                    "text": str(cell or "").strip(),
                                    "method": "pdfplumber",
                                    "quality": "medium",
                                    "notes": "",
                                }
                            )
    except Exception as exc:
        rows.append(
            {
                "page": "",
                "table_id": "",
                "row": "",
                "column": "",
                "text": "",
                "method": "pdfplumber",
                "quality": "failed",
                "notes": f"pdfplumber_failed:{exc}",
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--stem", help="Output filename stem; defaults to input stem")
    parser.add_argument("--max-chars", type=int, default=2000)
    parser.add_argument("--ocr", choices=["never", "auto", "always"], default="never")
    parser.add_argument("--ocr-lang", default="eng")
    parser.add_argument("--tessdata", help="Optional Tesseract tessdata path for PyMuPDF OCR")
    parser.add_argument("--table-fallback", choices=["none", "pdfplumber"], default="pdfplumber")
    args = parser.parse_args()

    fitz = require_pymupdf()
    if not args.input.exists():
        raise SystemExit(f"Input PDF not found: {args.input}")
    if args.input.suffix.lower() != ".pdf":
        raise SystemExit("Input must be a PDF file.")

    stem = args.stem or args.input.stem
    args.output_dir.mkdir(parents=True, exist_ok=True)
    text_csv = args.output_dir / f"{stem}_page_text.csv"
    table_csv = args.output_dir / f"{stem}_tables.csv"
    recovery_md = args.output_dir / f"{stem}_manual_recovery.md"
    manifest_json = args.output_dir / f"{stem}_manifest.json"

    text_rows: list[dict[str, Any]] = []
    table_rows: list[dict[str, Any]] = []
    recovery: list[str] = []
    table_statuses: list[str] = []

    with fitz.open(str(args.input)) as doc:
        for page_index, page in enumerate(doc, start=1):
            method = "pymupdf_text"
            notes: list[str] = []
            text = page.get_text("text")
            base_quality = quality_label(text)
            if args.ocr == "always" or (args.ocr == "auto" and base_quality in {"failed", "low"}):
                ocr_result, ocr_note = ocr_text(page, args.ocr_lang, args.tessdata)
                notes.append(ocr_note)
                if quality_label(ocr_result) != "failed":
                    text = ocr_result
                    method = "pymupdf_ocr"
            quality = quality_label(text)
            if quality in {"failed", "low"}:
                recovery.append(f"- page {page_index}: text quality={quality}; manual/OCR review recommended.")
            text_rows.append(
                {
                    "source_path": str(args.input),
                    "source_type": "pdf",
                    "location": f"page {page_index}",
                    "heading": "",
                    "content_type": "page_text",
                    "text": clean_text(text, args.max_chars),
                    "metadata": f"chars={len(text)};method={method}",
                    "quality": quality,
                    "notes": ";".join(notes),
                }
            )

            page_tables, table_status = extract_pymupdf_tables(page, page_index)
            table_statuses.append(f"page {page_index}: {table_status}")
            table_rows.extend(page_tables)

    if not table_rows and args.table_fallback == "pdfplumber":
        fallback_rows = extract_pdfplumber_tables(args.input)
        table_rows.extend(fallback_rows)
        if fallback_rows:
            table_statuses.append("pdfplumber fallback produced table rows")
        else:
            recovery.append("- tables: no tables extracted; try manual crop/table settings or provide source tables.")

    write_csv(
        text_csv,
        ["source_path", "source_type", "location", "heading", "content_type", "text", "metadata", "quality", "notes"],
        text_rows,
    )
    write_csv(
        table_csv,
        ["page", "table_id", "row", "column", "text", "method", "quality", "notes"],
        table_rows,
    )
    recovery_md.write_text("# Manual Recovery List\n\n" + ("\n".join(recovery) if recovery else "No manual recovery items detected.\n"), encoding="utf-8")
    manifest = {
        "input": str(args.input),
        "pymupdf_version": getattr(fitz, "__doc__", "").splitlines()[0] if getattr(fitz, "__doc__", "") else "",
        "text_csv": str(text_csv),
        "table_csv": str(table_csv),
        "manual_recovery": str(recovery_md),
        "pages": len(text_rows),
        "table_cells": len(table_rows),
        "ocr_mode": args.ocr,
        "table_statuses": table_statuses,
    }
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"text={text_csv} tables={table_csv} recovery={recovery_md} manifest={manifest_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
