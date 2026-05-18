#!/usr/bin/env python3
"""Cross-check literature identity across Crossref, OpenAlex, Semantic Scholar, and PubMed.

Input may be CSV/TSV with columns such as id,title,doi,authors,year,venue, or a
plain-text list containing DOI strings and/or titles. Network access is required.
The output is a CSV identity-audit table; it does not mark sources as writing-ready
unless the metadata agreement is explicit.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)


@dataclass
class InputRecord:
    record_id: str
    title: str
    doi: str
    raw: str


@dataclass
class SourceResult:
    source: str
    title: str = ""
    doi: str = ""
    year: str = ""
    venue: str = ""
    url: str = ""
    status: str = "not_checked"
    error: str = ""


def normalize_doi(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    value = value.removeprefix("doi:")
    return value.rstrip(".,;)]}")


def normalize_title(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return " ".join(value.split())


def title_similarity(left: str, right: str) -> float:
    left_norm = normalize_title(left)
    right_norm = normalize_title(right)
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def request_json(url: str, user_agent: str, timeout: int) -> dict:
    req = Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def request_text(url: str, user_agent: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def first(value) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    return str(value or "")


def crossref_message_to_result(message: dict) -> SourceResult:
    return SourceResult(
        source="crossref",
        title=first(message.get("title", [])),
        doi=normalize_doi(message.get("DOI", "")),
        year=year_from_crossref(message),
        venue=first(message.get("container-title", [])),
        url=message.get("URL", ""),
        status="ok",
    )


def year_from_crossref(message: dict) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = message.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def check_crossref(record: InputRecord, user_agent: str, timeout: int) -> SourceResult:
    try:
        if record.doi:
            url = f"https://api.crossref.org/works/{quote(record.doi, safe='')}"
            payload = request_json(url, user_agent, timeout)
            return crossref_message_to_result(payload.get("message", {}))
        if record.title:
            query = urlencode({"query.bibliographic": record.title, "rows": "1"})
            payload = request_json(f"https://api.crossref.org/works?{query}", user_agent, timeout)
            items = payload.get("message", {}).get("items", [])
            if items:
                return crossref_message_to_result(items[0])
            return SourceResult("crossref", status="not_found")
        return SourceResult("crossref", status="no_query")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SourceResult("crossref", status="error", error=str(exc))


def openalex_to_result(item: dict) -> SourceResult:
    doi = item.get("doi") or ""
    host = item.get("primary_location", {}).get("source") or {}
    return SourceResult(
        source="openalex",
        title=item.get("title", ""),
        doi=normalize_doi(doi),
        year=str(item.get("publication_year") or ""),
        venue=host.get("display_name", ""),
        url=item.get("id", ""),
        status="ok",
    )


def check_openalex(record: InputRecord, user_agent: str, timeout: int) -> SourceResult:
    try:
        if record.doi:
            url = f"https://api.openalex.org/works/https://doi.org/{quote(record.doi, safe='/')}"
            payload = request_json(url, user_agent, timeout)
            return openalex_to_result(payload)
        if record.title:
            query = urlencode({"search": record.title, "per-page": "1"})
            payload = request_json(f"https://api.openalex.org/works?{query}", user_agent, timeout)
            results = payload.get("results", [])
            if results:
                return openalex_to_result(results[0])
            return SourceResult("openalex", status="not_found")
        return SourceResult("openalex", status="no_query")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SourceResult("openalex", status="error", error=str(exc))


def semantic_to_result(item: dict) -> SourceResult:
    venue = item.get("venue") or item.get("publicationVenue", {}).get("name", "")
    return SourceResult(
        source="semantic_scholar",
        title=item.get("title", ""),
        doi=normalize_doi(item.get("externalIds", {}).get("DOI", "")),
        year=str(item.get("year") or ""),
        venue=venue,
        url=item.get("url", ""),
        status="ok",
    )


def check_semantic_scholar(record: InputRecord, user_agent: str, timeout: int) -> SourceResult:
    fields = "title,year,venue,publicationVenue,externalIds,url"
    try:
        if record.doi:
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{quote(record.doi, safe='')}?fields={fields}"
            payload = request_json(url, user_agent, timeout)
            return semantic_to_result(payload)
        if record.title:
            query = urlencode({"query": record.title, "limit": "1", "fields": fields})
            payload = request_json(f"https://api.semanticscholar.org/graph/v1/paper/search?{query}", user_agent, timeout)
            data = payload.get("data", [])
            if data:
                return semantic_to_result(data[0])
            return SourceResult("semantic_scholar", status="not_found")
        return SourceResult("semantic_scholar", status="no_query")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SourceResult("semantic_scholar", status="error", error=str(exc))


def check_pubmed(record: InputRecord, user_agent: str, timeout: int) -> SourceResult:
    if not record.doi:
        return SourceResult("pubmed", status="doi_required")
    try:
        term = f"{record.doi}[doi]"
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urlencode(
            {"db": "pubmed", "term": term, "retmode": "json", "retmax": "1"}
        )
        search = request_json(search_url, user_agent, timeout)
        ids = search.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return SourceResult("pubmed", status="not_found")
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urlencode(
            {"db": "pubmed", "id": ids[0], "retmode": "xml"}
        )
        xml_text = request_text(fetch_url, user_agent, timeout)
        root = ET.fromstring(xml_text)
        article = root.find(".//Article")
        title = " ".join(article.findtext("ArticleTitle", default="").split()) if article is not None else ""
        journal = root.findtext(".//Journal/Title", default="")
        year = root.findtext(".//PubDate/Year", default="")
        return SourceResult("pubmed", title=title, doi=record.doi, year=year, venue=journal, url=f"https://pubmed.ncbi.nlm.nih.gov/{ids[0]}/", status="ok")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ET.ParseError) as exc:
        return SourceResult("pubmed", status="error", error=str(exc))


def parse_records(path: Path) -> list[InputRecord]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    suffix = path.suffix.lower()
    records: list[InputRecord] = []
    if suffix in {".csv", ".tsv"}:
        dialect = "excel-tab" if suffix == ".tsv" else "excel"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, dialect=dialect)
            for index, row in enumerate(reader, start=1):
                title = row.get("title") or row.get("Title") or row.get("article_title") or ""
                doi = row.get("doi") or row.get("DOI") or ""
                record_id = row.get("id") or row.get("key") or row.get("citation_key") or str(index)
                raw = " ".join(str(value) for value in row.values() if value)
                records.append(InputRecord(str(record_id), title.strip(), normalize_doi(doi), raw))
        return records

    seen: set[str] = set()
    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        doi_match = DOI_RE.search(stripped)
        doi = normalize_doi(doi_match.group(0)) if doi_match else ""
        title = DOI_RE.sub("", stripped).strip(" .,-;")
        key = doi or title.lower()
        if key in seen:
            continue
        seen.add(key)
        records.append(InputRecord(str(index), title, doi, stripped))
    return records


def choose_confidence(record: InputRecord, results: list[SourceResult]) -> tuple[str, str, str]:
    ok = [result for result in results if result.status == "ok"]
    if not ok:
        return "unresolved", "no authoritative source returned metadata", "manual search required"

    doi_matches = [result for result in ok if record.doi and normalize_doi(result.doi) == record.doi]
    title_scores = [title_similarity(record.title, result.title) for result in ok if record.title and result.title]
    high_title_matches = [score for score in title_scores if score >= 0.90]
    medium_title_matches = [score for score in title_scores if score >= 0.80]

    if record.doi and len(doi_matches) >= 2 and (not record.title or high_title_matches):
        return "verified_candidate", "doi agrees across at least two sources", "eligible for user review"
    if record.doi and len(doi_matches) == 1 and (not record.title or medium_title_matches):
        return "needs_review", "doi resolved in one source only", "check publisher page or another database"
    if not record.doi and len(high_title_matches) >= 2:
        return "needs_doi_decision", "title agrees across at least two sources but DOI was not supplied", "choose DOI after user review"
    return "mismatch_or_weak", "metadata agreement is weak or conflicting", "queue manual verification"


def row_for_record(record: InputRecord, results: list[SourceResult]) -> dict[str, str]:
    state, reason, action = choose_confidence(record, results)
    row = {
        "id": record.record_id,
        "input_title": record.title,
        "input_doi": record.doi,
        "proposed_state": state,
        "reason": reason,
        "next_action": action,
    }
    errors = []
    for result in results:
        prefix = result.source
        row[f"{prefix}_status"] = result.status
        row[f"{prefix}_title"] = result.title
        row[f"{prefix}_doi"] = result.doi
        row[f"{prefix}_year"] = result.year
        row[f"{prefix}_venue"] = result.venue
        row[f"{prefix}_url"] = result.url
        row[f"{prefix}_title_similarity"] = f"{title_similarity(record.title, result.title):.3f}" if record.title and result.title else ""
        if result.error:
            errors.append(f"{prefix}: {result.error}")
    row["errors"] = " | ".join(errors)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mailto", help="Email included in User-Agent for polite API access")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--pause", type=float, default=0.2)
    parser.add_argument(
        "--sources",
        default="crossref,openalex,semantic_scholar,pubmed",
        help="Comma-separated sources: crossref,openalex,semantic_scholar,pubmed",
    )
    args = parser.parse_args()

    records = parse_records(args.input)
    user_agent = "darwin-skill-multi-source-lit-check/1.0"
    if args.mailto:
        user_agent += f" (mailto:{args.mailto})"
    selected = {item.strip() for item in args.sources.split(",") if item.strip()}

    rows: list[dict[str, str]] = []
    for record in records:
        results: list[SourceResult] = []
        if "crossref" in selected:
            results.append(check_crossref(record, user_agent, args.timeout))
        if "openalex" in selected:
            results.append(check_openalex(record, user_agent, args.timeout))
        if "semantic_scholar" in selected:
            results.append(check_semantic_scholar(record, user_agent, args.timeout))
        if "pubmed" in selected:
            results.append(check_pubmed(record, user_agent, args.timeout))
        rows.append(row_for_record(record, results))
        if args.pause:
            time.sleep(args.pause)

    fieldnames = [
        "id",
        "input_title",
        "input_doi",
        "proposed_state",
        "reason",
        "next_action",
    ]
    for source in ["crossref", "openalex", "semantic_scholar", "pubmed"]:
        fieldnames.extend(
            [
                f"{source}_status",
                f"{source}_title",
                f"{source}_doi",
                f"{source}_year",
                f"{source}_venue",
                f"{source}_url",
                f"{source}_title_similarity",
            ]
        )
    fieldnames.append("errors")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"records={len(records)} output={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
