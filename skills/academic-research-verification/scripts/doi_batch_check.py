#!/usr/bin/env python3
"""Batch-check DOI metadata with the Crossref REST API.

Input can be a text file, CSV, or TSV containing DOI strings. The script extracts
DOI-like tokens, queries Crossref, and writes a CSV with the resolved source
trail. Network access is required.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)


def extract_dois(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    seen: set[str] = set()
    dois: list[str] = []
    for match in DOI_RE.finditer(text):
        doi = match.group(0).rstrip(".,;)]}").lower()
        if doi not in seen:
            seen.add(doi)
            dois.append(doi)
    return dois


def first(value):
    if isinstance(value, list) and value:
        return value[0]
    return ""


def fetch_crossref(doi: str, mailto: str | None, timeout: int) -> dict:
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
    ua = "darwin-skill-doi-batch-check/1.0"
    if mailto:
        ua += f" (mailto:{mailto})"
    request = Request(url, headers={"User-Agent": ua})
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("message", {})


def year_from_message(message: dict) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = message.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def row_for_doi(doi: str, mailto: str | None, timeout: int, pause: float) -> dict:
    row = {
        "input_doi": doi,
        "resolved": "no",
        "crossref_doi": "",
        "title": "",
        "authors": "",
        "year": "",
        "venue": "",
        "type": "",
        "url": "",
        "status": "",
        "error": "",
    }
    try:
        message = fetch_crossref(doi, mailto, timeout)
        row.update(
            {
                "resolved": "yes",
                "crossref_doi": message.get("DOI", ""),
                "title": first(message.get("title", [])),
                "authors": "; ".join(
                    " ".join(
                        part
                        for part in (author.get("given", ""), author.get("family", ""))
                        if part
                    )
                    for author in message.get("author", [])[:8]
                ),
                "year": year_from_message(message),
                "venue": first(message.get("container-title", [])),
                "type": message.get("type", ""),
                "url": message.get("URL", ""),
                "status": "ok",
            }
        )
    except HTTPError as exc:
        row["status"] = f"http_{exc.code}"
        row["error"] = str(exc)
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        row["status"] = "error"
        row["error"] = str(exc)
    if pause:
        time.sleep(pause)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Text/CSV/TSV file containing DOIs")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    parser.add_argument("--mailto", help="Email for polite Crossref User-Agent contact")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--pause", type=float, default=0.1, help="Pause between requests in seconds")
    args = parser.parse_args()

    dois = extract_dois(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "input_doi",
        "resolved",
        "crossref_doi",
        "title",
        "authors",
        "year",
        "venue",
        "type",
        "url",
        "status",
        "error",
    ]
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for doi in dois:
            writer.writerow(row_for_doi(doi, args.mailto, args.timeout, args.pause))

    print(f"checked={len(dois)} output={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
