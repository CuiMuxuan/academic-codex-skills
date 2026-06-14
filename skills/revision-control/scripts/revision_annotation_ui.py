#!/usr/bin/env python3
"""Local browser UI for collecting revision-control annotations.

The script uses only the Python standard library. It reads
revision_workbench/bilingual_revision/manuscript_objects.json and writes only
revision_workbench/bilingual_revision/rounds/<round>/user_annotations.json.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingTCPServer
from typing import Any
from urllib.parse import parse_qs, urlparse


PROBLEM_TYPES = [
    "language_style",
    "grammar",
    "ambiguity",
    "terminology",
    "citation_expression",
    "unsupported_claim",
    "unsupported_superiority_claim",
    "duplicate_argument",
    "context_fit",
    "paragraph_logic",
    "section_positioning",
    "needs_insert_sentence",
    "needs_delete",
    "needs_merge",
    "needs_split",
    "operation_record_residue",
    "figure_table_text",
    "other",
]

SUGGESTED_ACTIONS = [
    "direct_revision_candidate",
    "language_review_needed",
    "upgrade_required",
    "evidence_verification_needed",
    "literature_verification_needed",
    "structure_rewrite_needed",
    "final_polish_later",
    "keep_with_note",
    "other",
]

DEFAULT_ACTION_BY_ISSUE = {
    "language_style": "direct_revision_candidate",
    "grammar": "direct_revision_candidate",
    "ambiguity": "direct_revision_candidate",
    "terminology": "language_review_needed",
    "citation_expression": "evidence_verification_needed",
    "unsupported_claim": "upgrade_required",
    "unsupported_superiority_claim": "upgrade_required",
    "paragraph_logic": "structure_rewrite_needed",
    "section_positioning": "structure_rewrite_needed",
    "needs_insert_sentence": "direct_revision_candidate",
}


def now_iso() -> str:
    return dt.datetime.now(dt.datetime.now().astimezone().tzinfo).isoformat(timespec="seconds")


def normalize_text(text: Any) -> str:
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def stable_hash(text: Any) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def yaml_quote(value: Any) -> str:
    return json.dumps(str(value or ""), ensure_ascii=False)


def parse_yaml_scalar(value: str) -> Any:
    value = value.strip()
    if value == "[]":
        return []
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value in {"''", '""'}:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            return json.loads(value)
        except Exception:
            return value[1:-1]
    return value


def parse_key_value(text: str) -> tuple[str, Any] | None:
    if ":" not in text:
        return None
    key, value = text.split(":", 1)
    return key.strip(), parse_yaml_scalar(value.strip())


def as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [part.strip() for part in re.split(r"[\n,;；]+", text) if part.strip()]


def normalize_terminology_item(item: dict[str, Any]) -> dict[str, Any]:
    term = str(item.get("term", "")).strip()
    preferred = str(item.get("preferred_form", "")).strip()
    return {
        "term": term,
        "language": str(item.get("language", "")).strip(),
        "preferred_form": preferred or term,
        "accepted_variants": as_string_list(item.get("accepted_variants", [])),
        "chinese_translations": as_string_list(item.get("chinese_translations", [])),
        "forbidden_variants": as_string_list(item.get("forbidden_variants", [])),
        "field": str(item.get("field", "")).strip(),
        "term_type": str(item.get("term_type", "")).strip(),
        "source_provenance": as_string_list(item.get("source_provenance", [])),
        "reason": str(item.get("reason", "")).strip(),
        "confirmed": bool(item.get("confirmed", False)),
    }


def parse_terminology_yaml(text: str) -> list[dict[str, Any]]:
    terms: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    pending_list_key = ""
    in_glossary = False
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()
        if not raw_line.startswith(" ") and stripped.endswith(":"):
            in_glossary = stripped[:-1] == "terminology_glossary"
            pending_list_key = ""
            continue
        if not in_glossary:
            continue
        if stripped.startswith("- "):
            body = stripped[2:].strip()
            if pending_list_key and current is not None and raw_line.startswith("    "):
                current.setdefault(pending_list_key, []).append(parse_yaml_scalar(body))
                continue
            current = {}
            terms.append(current)
            pending_list_key = ""
            if body:
                parsed = parse_key_value(body)
                if parsed:
                    key, value = parsed
                    current[key] = value
            continue
        if current is None:
            continue
        parsed = parse_key_value(stripped)
        if not parsed:
            continue
        key, value = parsed
        if value == "":
            current[key] = []
            pending_list_key = key
        else:
            current[key] = value
            pending_list_key = key if isinstance(value, list) else ""
    return [item for item in (normalize_terminology_item(term) for term in terms) if item["term"]]


def dump_terminology_yaml(terms: list[dict[str, Any]]) -> str:
    lines = ["terminology_glossary:"]
    if not terms:
        lines.append("  []")
        return "\n".join(lines) + "\n"
    for raw_item in terms:
        item = normalize_terminology_item(raw_item)
        lines.append(f"  - term: {yaml_quote(item['term'])}")
        lines.append(f"    language: {yaml_quote(item['language'])}")
        lines.append(f"    preferred_form: {yaml_quote(item['preferred_form'])}")
        for key in ("accepted_variants", "chinese_translations", "forbidden_variants", "source_provenance"):
            values = as_string_list(item.get(key, []))
            if values:
                lines.append(f"    {key}:")
                for value in values:
                    lines.append(f"      - {yaml_quote(value)}")
            else:
                lines.append(f"    {key}: []")
        lines.append(f"    field: {yaml_quote(item['field'])}")
        lines.append(f"    term_type: {yaml_quote(item['term_type'])}")
        lines.append(f"    reason: {yaml_quote(item['reason'])}")
        lines.append(f"    confirmed: {str(bool(item['confirmed'])).lower()}")
    return "\n".join(lines) + "\n"


def markdown_escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def dump_terminology_markdown(terms: list[dict[str, Any]]) -> str:
    lines = [
        "# Terminology Glossary",
        "",
        "| term | language | preferred form | accepted variants | Chinese translations | field | term type | source provenance | forbidden variants | confirmed | reason |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for raw_item in terms:
        item = normalize_terminology_item(raw_item)
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape_cell(item["term"]),
                    markdown_escape_cell(item["language"]),
                    markdown_escape_cell(item["preferred_form"]),
                    markdown_escape_cell(", ".join(item["accepted_variants"])),
                    markdown_escape_cell(", ".join(item["chinese_translations"])),
                    markdown_escape_cell(item["field"]),
                    markdown_escape_cell(item["term_type"]),
                    markdown_escape_cell("; ".join(item["source_provenance"])),
                    markdown_escape_cell(", ".join(item["forbidden_variants"])),
                    "yes" if item["confirmed"] else "no",
                    markdown_escape_cell(item["reason"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def first_value(item: dict[str, Any], *names: str, default: str = "") -> str:
    for name in names:
        value = item.get(name)
        if value is not None and str(value) != "":
            return str(value)
    return default


def node(
    node_type: str,
    node_id: str,
    title: str = "",
    text: str = "",
    **extra: Any,
) -> dict[str, Any]:
    payload = {
        "node_type": node_type,
        "id": node_id,
        "title": title,
        "text": text,
        "children": [],
    }
    payload.update(extra)
    return payload


class AppState:
    def __init__(self, workbench: Path, round_id: str, create_round: bool) -> None:
        self.workbench = workbench.resolve()
        self.round_id = round_id
        self.create_round = create_round
        self.bilingual_dir = self.workbench / "bilingual_revision"
        self.shared_dir = self.workbench / "shared"
        self.object_path = self.bilingual_dir / "manuscript_objects.json"
        self.round_dir = self.bilingual_dir / "rounds" / round_id
        self.annotation_path = self.round_dir / "user_annotations.json"
        self.modification_log_path = self.round_dir / "modification_log.md"
        self.terminology_yaml_path = self.shared_dir / "terminology_glossary.yaml"
        self.terminology_md_path = self.shared_dir / "terminology_glossary.md"

    def source_object_library(self) -> str:
        try:
            return self.object_path.relative_to(self.workbench).as_posix()
        except ValueError:
            return self.object_path.as_posix()

    def terminology_source_path(self) -> str:
        try:
            return self.terminology_yaml_path.relative_to(self.workbench).as_posix()
        except ValueError:
            return self.terminology_yaml_path.as_posix()

    def read_object_library(self) -> dict[str, Any]:
        with self.object_path.open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("manuscript_objects.json must contain a JSON object")
        return data

    def paper_meta(self) -> dict[str, Any]:
        try:
            data = self.read_object_library()
        except Exception:
            return {"paper_id": "", "title": ""}
        paper = data.get("paper", data)
        if not isinstance(paper, dict):
            return {"paper_id": "", "title": ""}
        return {
            "paper_id": first_value(paper, "paper_id", "id", default=""),
            "title": first_value(paper, "title", "name", default="未命名文稿 / Untitled manuscript"),
            "language_mode": first_value(paper, "language_mode", default=""),
            "current_round": first_value(paper, "current_round", default=self.round_id),
        }

    def empty_annotation_document(self) -> dict[str, Any]:
        paper = self.paper_meta()
        stamp = now_iso()
        return {
            "schema_version": "1.0",
            "paper_id": paper.get("paper_id", ""),
            "round": self.round_id,
            "source_object_library": self.source_object_library(),
            "view_mode": "full_manuscript",
            "created_at": stamp,
            "updated_at": stamp,
            "annotations": [],
            "resolved_annotations": [],
            "sentence_status_decisions": {},
        }

    def load_annotations(self) -> dict[str, Any]:
        if not self.annotation_path.exists():
            return self.empty_annotation_document()
        with self.annotation_path.open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("user_annotations.json must contain a JSON object")
        data.setdefault("schema_version", "1.0")
        data.setdefault("paper_id", self.paper_meta().get("paper_id", ""))
        data.setdefault("round", self.round_id)
        data.setdefault("source_object_library", self.source_object_library())
        data.setdefault("view_mode", "full_manuscript")
        data.setdefault("created_at", now_iso())
        data.setdefault("updated_at", now_iso())
        data.setdefault("annotations", [])
        data.setdefault("resolved_annotations", [])
        data.setdefault("sentence_status_decisions", {})
        if not isinstance(data["annotations"], list):
            data["annotations"] = []
        if not isinstance(data["resolved_annotations"], list):
            data["resolved_annotations"] = []
        data["sentence_status_decisions"] = sentence_status_decisions(data)
        return data

    def has_modification_log_entries(self) -> bool:
        if not self.modification_log_path.exists():
            return False
        text = self.modification_log_path.read_text(encoding="utf-8-sig", errors="replace")
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            compact = line.replace("|", "").replace("-", "").replace(":", "").strip()
            if not compact:
                continue
            lower = line.lower()
            if "timestamp" in lower and "sentence_id" in lower and "revision_count" in lower:
                continue
            return True
        return False

    def decorate_annotation_document(self, document: dict[str, Any], id_map: dict[str, str] | None = None) -> dict[str, Any]:
        document["annotation_path"] = self.annotation_path.as_posix()
        document["modification_log_exists"] = self.has_modification_log_entries()
        if id_map is not None:
            document["annotation_id_map"] = id_map
        return document

    def save_annotations(self, document: dict[str, Any]) -> dict[str, Any]:
        if not self.round_dir.exists():
            if not self.create_round:
                raise FileNotFoundError(
                    f"round directory does not exist: {self.round_dir}. "
                    "Restart with --create-round to create it."
                )
            self.round_dir.mkdir(parents=True, exist_ok=True)
        document["updated_at"] = now_iso()
        document.setdefault("created_at", now_iso())
        document["round"] = self.round_id
        document["source_object_library"] = self.source_object_library()
        document["annotations"] = document.get("annotations", [])
        document["resolved_annotations"] = document.get("resolved_annotations", [])
        if not isinstance(document["annotations"], list):
            document["annotations"] = []
        if not isinstance(document["resolved_annotations"], list):
            document["resolved_annotations"] = []
        document["sentence_status_decisions"] = sentence_status_decisions(document)
        mark_annotated_sentences_failed(document)
        id_map = renumber_annotation_ids(document)
        for key in ("annotation_path", "modification_log_exists", "annotation_id_map"):
            document.pop(key, None)
        tmp = self.annotation_path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        tmp.replace(self.annotation_path)
        return self.decorate_annotation_document(document, id_map)

    def load_terminology_glossary(self) -> dict[str, Any]:
        exists = self.terminology_yaml_path.exists()
        terms: list[dict[str, Any]] = []
        if exists:
            text = self.terminology_yaml_path.read_text(encoding="utf-8-sig", errors="replace")
            terms = parse_terminology_yaml(text)
        return {
            "exists": exists,
            "source_path": self.terminology_source_path(),
            "markdown_path": self.terminology_md_path.as_posix(),
            "terms": terms,
        }

    def save_terminology_glossary(self, terms: list[dict[str, Any]]) -> dict[str, Any]:
        self.shared_dir.mkdir(parents=True, exist_ok=True)
        normalized = sorted(
            [item for item in (normalize_terminology_item(term) for term in terms) if item["term"]],
            key=lambda item: (item["term"].casefold(), item["preferred_form"].casefold()),
        )
        yaml_tmp = self.terminology_yaml_path.with_suffix(".yaml.tmp")
        yaml_tmp.write_text(dump_terminology_yaml(normalized), encoding="utf-8", newline="\n")
        yaml_tmp.replace(self.terminology_yaml_path)
        md_tmp = self.terminology_md_path.with_suffix(".md.tmp")
        md_tmp.write_text(dump_terminology_markdown(normalized), encoding="utf-8", newline="\n")
        md_tmp.replace(self.terminology_md_path)
        return self.load_terminology_glossary()

    def failed_sentence_ids(self) -> set[str]:
        ids: set[str] = set()
        candidates = [
            self.bilingual_dir / "partial_failed_sentence_review.md",
            self.round_dir / "sentence_check_results.md",
        ]
        pattern = re.compile(r"\bS[\w.-]*\d[\w.-]*\b")
        for path in candidates:
            if path.exists():
                text = path.read_text(encoding="utf-8-sig", errors="replace")
                ids.update(pattern.findall(text))
        try:
            annotations = self.load_annotations().get("annotations", [])
        except Exception:
            annotations = []
        for annotation in annotations:
            target = annotation.get("target", {}) if isinstance(annotation, dict) else {}
            for key in ("sentence_id", "after_sentence_id", "before_sentence_id"):
                value = target.get(key)
                if value:
                    ids.add(str(value))
        return ids

    def failed_sentence_ids_for_tree(self, tree: dict[str, Any]) -> set[str]:
        ids = collect_sentence_ids(tree) | self.failed_sentence_ids()
        decisions = sentence_status_decisions(self.load_annotations())
        pass_ids = {sentence_id for sentence_id, decision in decisions.items() if decision.get("status") == "pass"}
        fail_ids = {sentence_id for sentence_id, decision in decisions.items() if decision.get("status") == "fail"}
        return (ids | fail_ids) - pass_ids


def object_list(objects: dict[str, Any], *names: str) -> list[dict[str, Any]]:
    for name in names:
        value = objects.get(name)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


FRONT_MATTER_CHAPTER_ID = "__front_matter"
FIGURE_TABLE_CHAPTER_ID = "__figure_table_chapter"


def normalize_sentence_status(value: Any) -> str:
    return "pass" if str(value or "").strip().lower() == "pass" else "fail"


def sentence_status_decisions(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_decisions = document.get("sentence_status_decisions", {})
    if not isinstance(raw_decisions, dict):
        return {}
    decisions: dict[str, dict[str, Any]] = {}
    for sentence_id, raw_decision in raw_decisions.items():
        if not sentence_id:
            continue
        if isinstance(raw_decision, str):
            decisions[str(sentence_id)] = {"status": normalize_sentence_status(raw_decision)}
        elif isinstance(raw_decision, dict):
            decision = dict(raw_decision)
            decision["status"] = normalize_sentence_status(decision.get("status"))
            decisions[str(sentence_id)] = decision
        else:
            decisions[str(sentence_id)] = {"status": "fail"}
    return decisions


def target_sentence_id(annotation: dict[str, Any]) -> str:
    target = annotation.get("target", {})
    if not isinstance(target, dict):
        return ""
    return str(target.get("sentence_id", "")).strip()


def mark_annotated_sentences_failed(document: dict[str, Any]) -> None:
    decisions = sentence_status_decisions(document)
    changed = False
    stamp = now_iso()
    for annotation in document.get("annotations", []):
        if not isinstance(annotation, dict):
            continue
        sentence_id = target_sentence_id(annotation)
        if not sentence_id:
            continue
        decision = dict(decisions.get(sentence_id, {}))
        if decision.get("status") != "fail":
            decision["status"] = "fail"
            decision["updated_at"] = stamp
            decisions[sentence_id] = decision
            changed = True
    if changed:
        document["sentence_status_decisions"] = decisions


def collect_sentence_ids(tree: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    if tree.get("node_type") == "sentence":
        sentence_id = first_value(tree, "sentence_id", "id", default="")
        if sentence_id:
            ids.add(sentence_id)
    for child in tree.get("children", []):
        if isinstance(child, dict):
            ids.update(collect_sentence_ids(child))
    return ids


def normalized_heading(value: Any) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"[/\\|:：()\[\]{}]+", " ", text)
    text = re.sub(r"[_\-.]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_front_matter_heading(value: Any) -> bool:
    heading = normalized_heading(value)
    if not heading:
        return False
    exact = {
        "front matter",
        "frontmatter",
        "preliminaries",
        "preliminary matter",
        "title",
        "abstract",
        "summary",
        "highlights",
        "highlight",
        "keywords",
        "key words",
        "graphical abstract",
        "toc",
        "table of contents",
        "contents",
        "acknowledgement",
        "acknowledgements",
        "abbreviations",
        "abbreviation",
        "nomenclature",
        "list of figures",
        "list of tables",
        "正文前",
        "前置部分",
        "标题",
        "摘要",
        "关键词",
        "亮点",
        "目录",
        "致谢",
    }
    if heading in exact:
        return True
    return any(
        token in heading
        for token in ("abstract", "highlights", "keywords", "abbreviations", "摘要", "关键词", "缩略语")
    )


def front_matter_display_title(value: Any) -> str:
    heading = normalized_heading(value)
    if heading in {"title", "标题"}:
        return "标题 / Title"
    if heading in {"abstract", "summary", "摘要"}:
        return "摘要 / Abstract"
    if heading in {"highlights", "highlight", "亮点"}:
        return "Highlights"
    if heading in {"keywords", "key words", "关键词"}:
        return "关键词 / Keywords"
    if "graphical abstract" in heading:
        return "图文摘要 / Graphical abstract"
    if heading in {"abbreviations", "abbreviation"}:
        return "缩略语 / Abbreviations"
    if heading in {"toc", "table of contents", "contents", "目录"}:
        return "目录 / Contents"
    if heading in {"front matter", "frontmatter", "preliminaries", "preliminary matter", "正文前", "前置部分"}:
        return "正文前内容 / Front matter content"
    return str(value or "").strip() or "正文前内容 / Front matter content"


def is_numbered_body_chapter(value: Any) -> bool:
    heading = normalized_heading(value)
    if not heading:
        return False
    patterns = [
        r"^(chapter|ch)\s*\d+\b",
        r"^第\s*[一二三四五六七八九十百\d]+\s*章\b",
        r"^\d+\s*(\.|、|\s|:|：|-|$)",
    ]
    return any(re.search(pattern, heading) for pattern in patterns)


def is_body_chapter_start(value: Any) -> bool:
    heading = normalized_heading(value)
    if not heading:
        return False
    if is_numbered_body_chapter(value) and any(
        re.search(pattern, heading)
        for pattern in (r"^(chapter|ch)\s*1\b", r"^第\s*[一1]\s*章\b", r"^1\s*(\.|、|\s|:|：|-|$)")
    ):
        return True
    return heading in {"introduction", "intro", "引言", "绪论", "导论"}


def leading_front_matter_indexes(chapters: list[dict[str, Any]]) -> set[int]:
    first_body_index: int | None = None
    for index, chapter in enumerate(chapters):
        title = chapter.get("title") or chapter.get("id") or ""
        if is_body_chapter_start(title):
            first_body_index = index
            break
    if first_body_index is not None:
        return set(range(first_body_index))

    front_indexes: set[int] = set()
    for index, chapter in enumerate(chapters):
        title = chapter.get("title") or chapter.get("id") or ""
        if is_front_matter_heading(title):
            front_indexes.add(index)
            continue
        if is_body_chapter_start(title):
            break
        if front_indexes:
            break
        break
    return front_indexes


def body_chapter_bounds(chapters: list[dict[str, Any]]) -> tuple[int | None, int | None]:
    body_indexes = [
        index
        for index, chapter in enumerate(chapters)
        if is_numbered_body_chapter(chapter.get("title") or chapter.get("id") or "")
    ]
    if body_indexes:
        return min(body_indexes), max(body_indexes)
    for index, chapter in enumerate(chapters):
        if is_body_chapter_start(chapter.get("title") or chapter.get("id") or ""):
            return index, index
    return None, None


def clone_node_tree(item: dict[str, Any]) -> dict[str, Any]:
    copied = dict(item)
    copied["children"] = [clone_node_tree(child) for child in item.get("children", []) if isinstance(child, dict)]
    return copied


def front_matter_sections_from_chapter(chapter_node: dict[str, Any], fallback_index: int) -> list[dict[str, Any]]:
    chapter_title = chapter_node.get("title") or chapter_node.get("id") or ""
    children = [child for child in chapter_node.get("children", []) if isinstance(child, dict)]
    sections = [child for child in children if child.get("node_type") == "section"]
    if sections:
        normalized_sections: list[dict[str, Any]] = []
        for section in sections:
            copied = clone_node_tree(section)
            title = copied.get("title") or chapter_title
            if is_front_matter_heading(title):
                copied["title"] = front_matter_display_title(title)
            copied["source_chapter_id"] = chapter_node.get("id") or chapter_node.get("chapter_id") or ""
            normalized_sections.append(copied)
        return normalized_sections
    section_id = f"{FRONT_MATTER_CHAPTER_ID}_section_{fallback_index}"
    wrapper = node(
        "section",
        section_id,
        title=front_matter_display_title(chapter_title),
        section_id=section_id,
        source_chapter_id=chapter_node.get("id") or chapter_node.get("chapter_id") or "",
    )
    wrapper["children"] = [clone_node_tree(child) for child in children]
    return [wrapper]


def normalize_front_matter_section(section_node: dict[str, Any]) -> dict[str, Any]:
    copied = clone_node_tree(section_node)
    title = copied.get("title") or copied.get("id") or ""
    if is_front_matter_heading(title):
        copied["title"] = front_matter_display_title(title)
    return copied


def compact_identifier(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned[:56] or fallback


def is_figure_table_heading(value: Any) -> bool:
    heading = normalized_heading(value)
    if not heading:
        return False
    exact = {
        "figures",
        "figure",
        "tables",
        "table",
        "figure and table text",
        "figures and tables",
        "tables and figures",
        "图表",
        "图",
        "表",
        "图表章",
    }
    return heading in exact or heading.startswith(("appendix table", "supplementary table"))


FIGURE_TABLE_LABEL_RE = re.compile(
    r"((?:fig(?:ure)?|table|tbl)\.?\s*[-_.]?\s*[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*)",
    re.IGNORECASE,
)
ZH_FIGURE_TABLE_LABEL_RE = re.compile(r"([图表]\s*\d+(?:[-.][A-Za-z0-9]+)?)")
FIGURE_TABLE_TITLE_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(fig(?:ure)?|table|tbl)\.?\s*[-_.]?\s*([A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*)\s*(?:[.:：]|\*\*)",
    re.IGNORECASE,
)


def normalize_figure_table_label(raw: Any) -> str:
    value = str(raw or "").strip().rstrip(".")
    if not value:
        return ""
    match = re.match(r"^(fig(?:ure)?|table|tbl)\.?\s*[-_.]?\s*(.+)$", value, re.IGNORECASE)
    if match:
        kind = match.group(1).casefold()
        number = match.group(2).replace("_", ".").strip()
        if kind == "tbl":
            return f"Table {number}"
        if kind.startswith("fig"):
            return f"Fig. {number}"
        return f"Table {number}"
    return value


def figure_table_label_from_text(text: Any) -> str:
    value = str(text or "")
    match = FIGURE_TABLE_LABEL_RE.search(value)
    if match:
        return normalize_figure_table_label(re.sub(r"\s+", " ", match.group(1).replace("_", " ")).strip())
    match = ZH_FIGURE_TABLE_LABEL_RE.search(value)
    if match:
        return re.sub(r"\s+", "", match.group(1)).strip()
    return ""


def figure_table_title_label_from_text(text: Any) -> str:
    value = str(text or "").strip()
    match = FIGURE_TABLE_TITLE_RE.search(value)
    if match:
        return normalize_figure_table_label(f"{match.group(1)} {match.group(2)}")
    return ""


def collect_node_text(item: dict[str, Any]) -> str:
    pieces: list[str] = []
    text = item.get("text")
    if text:
        pieces.append(str(text))
    for child in item.get("children", []):
        if isinstance(child, dict):
            child_text = collect_node_text(child)
            if child_text:
                pieces.append(child_text)
    return " ".join(pieces)


def paragraph_figure_table_label(paragraph_node: dict[str, Any]) -> str:
    fields = [
        paragraph_node.get("source_text", ""),
        paragraph_node.get("title", ""),
        paragraph_node.get("id", ""),
        collect_node_text(paragraph_node),
    ]
    for field in fields:
        label = figure_table_label_from_text(field)
        if label:
            return label
    return ""


def paragraph_figure_table_title_label(paragraph_node: dict[str, Any]) -> str:
    fields = [
        paragraph_node.get("source_text", ""),
        collect_node_text(paragraph_node),
    ]
    for field in fields:
        label = figure_table_title_label_from_text(field)
        if label:
            return label
    return ""


def is_figure_table_paragraph(paragraph_node: dict[str, Any]) -> bool:
    role = normalized_heading(paragraph_node.get("paragraph_role", ""))
    source_type = normalized_heading(paragraph_node.get("source_block_type", ""))
    if "figure table" in role or "figure table" in source_type:
        return True
    return bool(paragraph_figure_table_label(paragraph_node))


def starts_figure_table_item(paragraph_node: dict[str, Any]) -> bool:
    role = normalized_heading(paragraph_node.get("paragraph_role", ""))
    source_type = normalized_heading(paragraph_node.get("source_block_type", ""))
    source_text = str(paragraph_node.get("source_text", "")).strip()
    if source_text.startswith("!["):
        return False
    return bool(paragraph_figure_table_title_label(paragraph_node)) and (
        "figure table text reference" in role
        or "figure or table text reference" in role
        or "figure table text reference" in source_type
        or "figure or table text reference" in source_type
    )


def figure_table_group_title(item: dict[str, Any], object_id: str, text: str, index: int) -> str:
    explicit = first_value(
        item,
        "figure_number",
        "table_number",
        "figure_id",
        "table_id",
        "display_label",
        "caption_label",
        "label",
        "number",
        default="",
    )
    if explicit:
        return explicit
    sources = [
        first_value(item, "title", "heading", default=""),
        text,
        object_id,
    ]
    for source in sources:
        label = figure_table_label_from_text(source)
        if label:
            return label
    item_type = first_value(item, "type", default="").casefold()
    if item_type.startswith("table"):
        return f"Table {index}"
    if item_type.startswith("figure") or item_type.startswith("fig"):
        return f"Figure {index}"
    return object_id or f"Figure/Table {index}"


def section_for_figure_table_label(label: str, used_labels: set[str], fallback_index: int) -> dict[str, Any]:
    title = label or f"图表 {fallback_index} / Figure or table {fallback_index}"
    section_id = f"FTSEC_{compact_identifier(title, str(fallback_index))}"
    if section_id in used_labels:
        section_id = f"{section_id}_{fallback_index}"
    used_labels.add(section_id)
    return node(
        "section",
        section_id,
        title=title,
        section_id=section_id,
        chapter_id=FIGURE_TABLE_CHAPTER_ID,
    )


def is_table_row_node(paragraph_node: dict[str, Any]) -> bool:
    role = normalized_heading(paragraph_node.get("paragraph_role", ""))
    source_type = normalized_heading(paragraph_node.get("source_block_type", ""))
    return "table row" in role or "table row" in source_type


def collect_figure_table_sections(
    chapter_node: dict[str, Any],
    used_labels: set[str],
    start_index: int,
    include_following_rows: bool,
) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    fallback_index = start_index
    for section_node in chapter_node.get("children", []):
        if not isinstance(section_node, dict):
            continue
        current_section: dict[str, Any] | None = None
        current_label = ""
        for paragraph_node in section_node.get("children", []):
            if not isinstance(paragraph_node, dict) or paragraph_node.get("node_type") != "paragraph":
                continue
            label = paragraph_figure_table_title_label(paragraph_node)
            if starts_figure_table_item(paragraph_node):
                fallback_index += 1
                current_label = label
                current_section = section_for_figure_table_label(current_label, used_labels, fallback_index)
                sections.append(current_section)
                current_section["children"].append(clone_node_tree(paragraph_node))
            elif current_section is not None and include_following_rows and (
                is_table_row_node(paragraph_node) or is_figure_table_paragraph(paragraph_node)
            ):
                current_section["children"].append(clone_node_tree(paragraph_node))
    return sections


def normalize_tree(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    paper = data.get("paper", data)
    if not isinstance(paper, dict):
        paper = {}
    objects = paper.get("objects") or data.get("objects") or {}
    if not isinstance(objects, dict):
        objects = {}

    paper_id = first_value(paper, "paper_id", "id", default="P001")
    paper_title = first_value(paper, "title", "name", default="未命名文稿 / Untitled manuscript")
    root = node("paper", paper_id, title=paper_title, paper_id=paper_id)

    chapters = object_list(objects, "chapters", "chapter")
    sections = object_list(objects, "sections", "section")
    paragraphs = object_list(objects, "paragraphs", "paragraph")
    sentences = object_list(objects, "sentences", "sentence")
    figure_texts = object_list(objects, "figure_table_text_objects", "figure_table_text")
    front_matter_chapter_indexes = leading_front_matter_indexes(chapters)
    body_start_index, body_end_index = body_chapter_bounds(chapters)

    chapter_nodes: dict[str, dict[str, Any]] = {}
    section_nodes: dict[str, dict[str, Any]] = {}
    paragraph_nodes: dict[str, dict[str, Any]] = {}
    sentence_nodes: dict[str, dict[str, Any]] = {}

    for index, chapter in enumerate(chapters, start=1):
        chapter_id = first_value(chapter, "chapter_id", "id", "node_id", default=f"CH_{index}")
        chapter_title = first_value(chapter, "title", "name", default=chapter_id)
        chapter_nodes[chapter_id] = node("chapter", chapter_id, title=chapter_title, chapter_id=chapter_id)

    for index, section in enumerate(sections, start=1):
        section_id = first_value(section, "section_id", "id", "node_id", default=f"SEC_{index}")
        section_title = first_value(section, "title", "heading", "name", default=section_id)
        chapter_id = first_value(section, "chapter_id", "parent_chapter_id", "parent_id", default="")
        section_nodes[section_id] = node(
            "section",
            section_id,
            title=section_title,
            section_id=section_id,
            chapter_id=chapter_id,
            local_purpose=section.get("local_purpose", ""),
            status=section.get("status", ""),
        )

    for index, paragraph in enumerate(paragraphs, start=1):
        paragraph_id = first_value(paragraph, "paragraph_id", "id", "node_id", default=f"P_{index}")
        paragraph_title = first_value(paragraph, "title", "paragraph_role", default=paragraph_id)
        section_id = first_value(paragraph, "section_id", "parent_section_id", "parent_id", default="")
        paragraph_nodes[paragraph_id] = node(
            "paragraph",
            paragraph_id,
            title=paragraph_title,
            paragraph_id=paragraph_id,
            section_id=section_id,
            paragraph_role=paragraph.get("paragraph_role", ""),
            source_block_type=paragraph.get("source_block_type", ""),
            source_text=paragraph.get("source_text", ""),
            status=paragraph.get("status", ""),
        )

    for index, sentence in enumerate(sentences, start=1):
        sentence_id = first_value(
            sentence,
            "sentence_id",
            "round_sentence_id",
            "id",
            "node_id",
            default=f"S{index:04d}",
        )
        text = first_value(sentence, "latest_text", "text", "original_text", default="")
        paragraph_id = first_value(sentence, "paragraph_id", "parent_paragraph_id", "parent_id", default="")
        sentence_nodes[sentence_id] = node(
            "sentence",
            sentence_id,
            text=text,
            sentence_id=sentence_id,
            paragraph_id=paragraph_id,
            user_confirmed_status=first_value(sentence, "user_confirmed_status", default=""),
            suggested_status=first_value(sentence, "suggested_status", default=""),
            status=normalize_sentence_status(
                first_value(sentence, "user_confirmed_status", "suggested_status", "status", default="fail")
            ),
            revision_count=sentence.get("revision_count", 0),
            hash=stable_hash(text),
        )

    used_sentence_ids: set[str] = set()
    for paragraph in paragraphs:
        paragraph_id = first_value(paragraph, "paragraph_id", "id", "node_id", default="")
        paragraph_node = paragraph_nodes.get(paragraph_id)
        if not paragraph_node:
            continue
        explicit_sentence_ids = paragraph.get("sentence_ids")
        if isinstance(explicit_sentence_ids, list):
            for sentence_id in explicit_sentence_ids:
                sentence_node = sentence_nodes.get(str(sentence_id))
                if sentence_node:
                    paragraph_node["children"].append(sentence_node)
                    used_sentence_ids.add(str(sentence_id))
        for sentence_id, sentence_node in sentence_nodes.items():
            if sentence_id in used_sentence_ids:
                continue
            if sentence_node.get("paragraph_id") == paragraph_id:
                paragraph_node["children"].append(sentence_node)
                used_sentence_ids.add(sentence_id)

    for sentence_id, sentence_node in sentence_nodes.items():
        if sentence_id not in used_sentence_ids:
            orphan_id = "_orphan_paragraph"
            if orphan_id not in paragraph_nodes:
                paragraph_nodes[orphan_id] = node(
                    "paragraph",
                    orphan_id,
                    title="未分配句子 / Unassigned sentences",
                    paragraph_id=orphan_id,
                )
            paragraph_nodes[orphan_id]["children"].append(sentence_node)

    used_paragraph_ids: set[str] = set()
    for section in sections:
        section_id = first_value(section, "section_id", "id", "node_id", default="")
        section_node = section_nodes.get(section_id)
        if not section_node:
            continue
        explicit_paragraph_ids = section.get("paragraph_ids")
        if isinstance(explicit_paragraph_ids, list):
            for paragraph_id in explicit_paragraph_ids:
                paragraph_node = paragraph_nodes.get(str(paragraph_id))
                if paragraph_node:
                    section_node["children"].append(paragraph_node)
                    used_paragraph_ids.add(str(paragraph_id))
        for paragraph_id, paragraph_node in paragraph_nodes.items():
            if paragraph_id in used_paragraph_ids:
                continue
            if paragraph_node.get("section_id") == section_id:
                section_node["children"].append(paragraph_node)
                used_paragraph_ids.add(paragraph_id)

    for paragraph_id, paragraph_node in paragraph_nodes.items():
        if paragraph_id not in used_paragraph_ids:
            if section_nodes:
                orphan_section_id = "_orphan_section"
                if orphan_section_id not in section_nodes:
                    section_nodes[orphan_section_id] = node(
                        "section",
                        orphan_section_id,
                        title="未分配段落 / Unassigned paragraphs",
                        section_id=orphan_section_id,
                    )
                section_nodes[orphan_section_id]["children"].append(paragraph_node)
            else:
                root["children"].append(paragraph_node)

    used_section_ids: set[str] = set()
    for chapter in chapters:
        chapter_id = first_value(chapter, "chapter_id", "id", "node_id", default="")
        chapter_node = chapter_nodes.get(chapter_id)
        if not chapter_node:
            continue
        explicit_section_ids = chapter.get("section_ids")
        if isinstance(explicit_section_ids, list):
            for section_id in explicit_section_ids:
                section_node = section_nodes.get(str(section_id))
                if section_node:
                    chapter_node["children"].append(section_node)
                    used_section_ids.add(str(section_id))
        for section_id, section_node in section_nodes.items():
            if section_id in used_section_ids:
                continue
            if section_node.get("chapter_id") == chapter_id:
                chapter_node["children"].append(section_node)
                used_section_ids.add(section_id)

    front_matter_children: list[dict[str, Any]] = []
    if paper_title:
        title_section = node(
            "section",
            f"{FRONT_MATTER_CHAPTER_ID}_title",
            title="标题 / Title",
            section_id=f"{FRONT_MATTER_CHAPTER_ID}_title",
            chapter_id=FRONT_MATTER_CHAPTER_ID,
        )
        title_paragraph_id = f"{FRONT_MATTER_CHAPTER_ID}_title_paragraph"
        title_sentence_id = f"{FRONT_MATTER_CHAPTER_ID}_title_sentence"
        title_paragraph = node(
            "paragraph",
            title_paragraph_id,
            title="标题 / Title",
            paragraph_id=title_paragraph_id,
            section_id=f"{FRONT_MATTER_CHAPTER_ID}_title",
            paragraph_role="front-matter title",
        )
        title_paragraph["children"].append(
            node(
                "sentence",
                title_sentence_id,
                text=paper_title,
                sentence_id=title_sentence_id,
                paragraph_id=title_paragraph_id,
                status="fail",
                revision_count=0,
                hash=stable_hash(paper_title),
            )
        )
        title_section["children"].append(
            title_paragraph
        )
        front_matter_children.append(title_section)
    body_chapter_nodes: list[dict[str, Any]] = []
    post_body_chapter_nodes: list[dict[str, Any]] = []
    used_figure_table_section_ids: set[str] = set()
    figure_chapter = node(
        "chapter",
        FIGURE_TABLE_CHAPTER_ID,
        title="图表章 / Figure and table text",
        chapter_id=FIGURE_TABLE_CHAPTER_ID,
    )
    if chapter_nodes:
        for chapter_index, chapter in enumerate(chapters):
            chapter_id = first_value(chapter, "chapter_id", "id", "node_id", default="")
            chapter_node = chapter_nodes.get(chapter_id)
            if not chapter_node:
                continue
            if chapter_index in front_matter_chapter_indexes or (
                body_start_index is not None and chapter_index < body_start_index
            ):
                front_matter_children.extend(front_matter_sections_from_chapter(chapter_node, chapter_index + 1))
            elif is_figure_table_heading(chapter_node.get("title") or chapter_node.get("id")):
                figure_chapter["children"].extend(
                    collect_figure_table_sections(
                        chapter_node,
                        used_figure_table_section_ids,
                        len(figure_chapter["children"]),
                        include_following_rows=True,
                    )
                )
            elif body_end_index is not None and chapter_index > body_end_index:
                extracted_sections = collect_figure_table_sections(
                    chapter_node,
                    used_figure_table_section_ids,
                    len(figure_chapter["children"]),
                    include_following_rows=False,
                )
                if extracted_sections:
                    figure_chapter["children"].extend(extracted_sections)
                else:
                    post_body_chapter_nodes.append(chapter_node)
            else:
                extracted_sections = collect_figure_table_sections(
                    chapter_node,
                    used_figure_table_section_ids,
                    len(figure_chapter["children"]),
                    include_following_rows=False,
                )
                if extracted_sections:
                    figure_chapter["children"].extend(extracted_sections)
                body_chapter_nodes.append(chapter_node)
        for section_id, section_node in section_nodes.items():
            if section_id not in used_section_ids:
                front_matter_children.append(normalize_front_matter_section(section_node))
        if front_matter_children:
            front_matter_chapter = node(
                "chapter",
                FRONT_MATTER_CHAPTER_ID,
                title="正文前 / Front matter",
                chapter_id=FRONT_MATTER_CHAPTER_ID,
            )
            front_matter_chapter["children"] = front_matter_children
            root["children"].append(front_matter_chapter)
        for chapter_node in body_chapter_nodes:
            root["children"].append(chapter_node)
        for chapter_node in post_body_chapter_nodes:
            root["children"].append(chapter_node)
        if figure_chapter["children"]:
            root["children"].append(figure_chapter)
    else:
        front_section_nodes: list[dict[str, Any]] = []
        body_section_nodes: list[dict[str, Any]] = []
        for section_node in section_nodes.values():
            if is_front_matter_heading(section_node.get("title") or section_node.get("id")):
                front_section_nodes.append(normalize_front_matter_section(section_node))
            elif is_figure_table_heading(section_node.get("title") or section_node.get("id")):
                section_wrapper = node(
                    "chapter",
                    f"{FIGURE_TABLE_CHAPTER_ID}_source",
                    title=section_node.get("title") or "图表文字 / Figure and table text",
                    chapter_id=f"{FIGURE_TABLE_CHAPTER_ID}_source",
                )
                section_wrapper["children"] = [section_node]
                figure_chapter["children"].extend(
                    collect_figure_table_sections(
                        section_wrapper,
                        used_figure_table_section_ids,
                        len(figure_chapter["children"]),
                        include_following_rows=True,
                    )
                )
            else:
                body_section_nodes.append(section_node)
        if front_section_nodes:
            front_matter_chapter = node(
                "chapter",
                FRONT_MATTER_CHAPTER_ID,
                title="正文前 / Front matter",
                chapter_id=FRONT_MATTER_CHAPTER_ID,
            )
            front_matter_chapter["children"] = front_section_nodes
            root["children"].append(front_matter_chapter)
        for section_node in body_section_nodes:
            root["children"].append(section_node)
        if figure_chapter["children"]:
            root["children"].append(figure_chapter)

    for index, item in enumerate(figure_texts, start=1):
        object_id = first_value(item, "object_id", "id", "node_id", default=f"FT_{index}")
        text = first_value(item, "latest_text", "text", "original_text", default="")
        group_title = figure_table_group_title(item, object_id, text, index)
        section_node = section_for_figure_table_label(
            group_title or object_id,
            used_figure_table_section_ids,
            len(figure_chapter["children"]) + index,
        )
        section_node["children"].append(
            node(
                "figure_table_text",
                object_id,
                title=first_value(item, "type", default=object_id),
                text=text,
                object_id=object_id,
                hash=stable_hash(text),
            )
        )
        figure_chapter["children"].append(section_node)
    if figure_texts and figure_chapter not in root["children"]:
        root["children"].append(figure_chapter)

    paper_meta = {
        "paper_id": paper_id,
        "title": paper_title,
        "language_mode": first_value(paper, "language_mode", default=""),
        "current_round": first_value(paper, "current_round", default=""),
    }
    return root, paper_meta


def filter_tree_for_sentences(tree: dict[str, Any], sentence_ids: set[str]) -> dict[str, Any] | None:
    if tree.get("node_type") == "sentence":
        return tree if tree.get("sentence_id") in sentence_ids or tree.get("id") in sentence_ids else None
    copied = dict(tree)
    copied["children"] = []
    for child in tree.get("children", []):
        filtered = filter_tree_for_sentences(child, sentence_ids)
        if filtered is not None:
            copied["children"].append(filtered)
    if copied.get("node_type") == "paper" or copied["children"]:
        return copied
    return None


def next_annotation_id(document: dict[str, Any]) -> str:
    max_id = 0
    for annotation in document.get("annotations", []):
        value = str(annotation.get("annotation_id", ""))
        match = re.fullmatch(r"A(\d+)", value)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"A{max_id + 1:04d}"


def renumber_annotation_ids(document: dict[str, Any]) -> dict[str, str]:
    annotations = document.get("annotations", [])
    if not isinstance(annotations, list):
        document["annotations"] = []
        return {}
    id_map: dict[str, str] = {}
    for index, annotation in enumerate(annotations, start=1):
        if not isinstance(annotation, dict):
            continue
        old_id = str(annotation.get("annotation_id", "")).strip()
        new_id = f"A{index:04d}"
        annotation["annotation_id"] = new_id
        if old_id:
            id_map[old_id] = new_id
    last_saved = str(document.get("last_saved_annotation_id", "")).strip()
    if last_saved and last_saved in id_map:
        document["last_saved_annotation_id"] = id_map[last_saved]
    elif annotations:
        document["last_saved_annotation_id"] = str(annotations[-1].get("annotation_id", ""))
    else:
        document.pop("last_saved_annotation_id", None)
    return id_map


HTML_PAGE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>论文修复批注 / Revision Annotation UI</title>
  <style>
    :root {
      color-scheme: light;
      --border: #d8dee8;
      --text: #1f2937;
      --muted: #667085;
      --panel: #f8fafc;
      --accent: #2f6fed;
      --p0: #fee2e2;
      --p1: #ffedd5;
      --p2: #fef9c3;
      --evidence: #dc2626;
      --structure: #7c3aed;
      --language: #2563eb;
      --term-bg: #dcfce7;
      --term-border: #86efac;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      color: var(--text);
      background: #fff;
    }
    header {
      height: 52px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 0 18px;
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 3;
    }
    header h1 {
      font-size: 16px;
      margin: 0;
      font-weight: 700;
    }
    header .meta {
      font-size: 12px;
      color: var(--muted);
      flex: 1;
    }
    select, textarea, button {
      font: inherit;
    }
    button {
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      border-radius: 6px;
      padding: 6px 9px;
      cursor: pointer;
    }
    button.primary {
      border-color: var(--accent);
      background: var(--accent);
      color: white;
    }
    button.danger {
      border-color: #fecaca;
      color: #b91c1c;
    }
    button:disabled {
      color: #98a2b3;
      background: #f2f4f7;
      cursor: not-allowed;
    }
    .top-tabs {
      display: inline-flex;
      gap: 6px;
      align-items: center;
    }
    .top-tab {
      min-height: 32px;
      white-space: nowrap;
    }
    .top-tab.active {
      border-color: var(--accent);
      background: #eff6ff;
      color: #1d4ed8;
    }
    .app-page[hidden] {
      display: none !important;
    }
    .annotation-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(300px, 0.42fr) minmax(320px, 0.5fr);
      min-height: calc(100vh - 52px);
    }
    .terminology-layout {
      display: grid;
      grid-template-columns: minmax(320px, 0.38fr) minmax(0, 1fr);
      gap: 18px;
      min-height: calc(100vh - 52px);
      padding: 18px 22px 60px;
      background: #fff;
    }
    #treePane {
      padding: 18px 22px 60px;
      overflow: auto;
    }
    #editorPane, #savedPane {
      border-left: 1px solid var(--border);
      background: var(--panel);
      padding: 16px;
      position: sticky;
      top: 52px;
      height: calc(100vh - 52px);
      overflow: auto;
    }
    #savedPane {
      background: #f8fafc;
    }
    .toolbar {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }
    .chapter-stepper {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
      padding: 10px 12px;
      margin-bottom: 16px;
    }
    .stepper-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 8px;
      font-size: 13px;
    }
    .stepper-head strong {
      font-size: 13px;
    }
    .stepper-count {
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }
    .stepper-buttons {
      display: flex;
      gap: 6px;
      align-items: center;
      overflow-x: auto;
      padding-bottom: 2px;
    }
    .stepper-buttons button {
      min-height: 32px;
      white-space: nowrap;
    }
    .step {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      max-width: 220px;
    }
    .step.active {
      border-color: var(--accent);
      background: #eff6ff;
      color: #1d4ed8;
    }
    .step-index {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 18px;
      border-radius: 999px;
      background: #e5e7eb;
      color: #344054;
      font-size: 11px;
      flex: 0 0 auto;
    }
    .step.active .step-index {
      background: var(--accent);
      color: #fff;
    }
    .step-label {
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .chapter-note {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }
    .virtual-chapter-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin: 0 0 10px;
    }
    .virtual-chapter-head h2 {
      margin: 0;
      font-size: 18px;
    }
    .virtual-list {
      height: calc(100vh - 210px);
      min-height: 360px;
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-gutter: stable;
      position: relative;
      padding-right: 6px;
    }
    .virtual-spacer {
      position: relative;
      min-height: 1px;
    }
    .virtual-row {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      will-change: transform;
      contain: layout style;
      overflow: visible;
    }
    .virtual-section-row {
      border-left: 2px solid #c7d2fe;
      margin: 10px 0 8px 6px;
      padding: 8px 10px;
      background: #f8fafc;
      font-weight: 700;
    }
    .virtual-section-row .node-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      width: 100%;
    }
    .virtual-debug {
      color: var(--muted);
      font-size: 12px;
      margin: 4px 0 8px;
    }
    details {
      border-left: 2px solid #e5e7eb;
      margin: 8px 0 8px 6px;
      padding-left: 10px;
    }
    summary {
      cursor: pointer;
      padding: 6px 0;
      font-weight: 700;
    }
    .node-row {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .node-id {
      color: var(--muted);
      font-size: 12px;
      font-weight: 400;
    }
    .paragraph {
      margin: 10px 0 12px 16px;
      padding: 10px 12px;
      border: 1px solid #eef2f7;
      border-radius: 8px;
      background: #fff;
      overflow: visible;
    }
    .paragraph-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }
    .sentence {
      display: block;
      line-height: 1.9;
      margin: 6px 0;
      padding: 4px 6px;
      border-radius: 4px;
      cursor: text;
    }
    .sentence-line {
      display: block;
    }
    .sentence-line + .sentence-line {
      margin-top: 2px;
    }
    .sentence-line.english {
      color: #475467;
    }
    .formula-inline {
      display: inline;
      padding: 1px 5px;
      border: 1px solid #cbd5e1;
      border-radius: 5px;
      background: #f8fafc;
      color: #111827;
      font-family: Consolas, "Liberation Mono", monospace;
      font-size: 0.95em;
      white-space: break-spaces;
    }
    .formula-block {
      display: block;
      margin: 6px 0;
      padding: 8px 10px;
      border: 1px solid #cbd5e1;
      border-radius: 7px;
      background: #f8fafc;
      color: #111827;
      font-family: Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      line-height: 1.45;
      text-align: center;
      white-space: pre-wrap;
      overflow-x: auto;
    }
    .sentence:hover {
      background: #eff6ff;
    }
    .sentence-tools {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 2px;
      color: var(--muted);
      font-size: 12px;
      user-select: none;
    }
    .sentence-status-badge {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 2px 7px;
      background: #f8fafc;
      white-space: nowrap;
    }
    .sentence-status-badge.pass {
      border-color: #bbf7d0;
      background: #f0fdf4;
      color: #15803d;
    }
    .sentence-status-badge.fail {
      border-color: #fecaca;
      background: #fef2f2;
      color: #b91c1c;
    }
    .status-toggle {
      padding: 2px 7px;
      border-radius: 999px;
      font-size: 12px;
      line-height: 1.35;
    }
    .status-toggle.active.pass {
      border-color: #22c55e;
      background: #dcfce7;
      color: #166534;
    }
    .status-toggle.active.fail {
      border-color: #ef4444;
      background: #fee2e2;
      color: #991b1b;
    }
    .gap-button {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 22px;
      height: 22px;
      margin: 4px 0 4px 18px;
      padding: 0;
      border-radius: 50%;
      color: var(--accent);
      font-weight: 700;
    }
    .node-comment {
      font-size: 12px;
      padding: 3px 6px;
    }
    .figure-text {
      margin: 12px 0 12px 16px;
      padding: 10px 12px;
      border: 1px dashed var(--border);
      border-radius: 8px;
      background: #fff;
      overflow: visible;
    }
    .annotation-p0 { background: var(--p0); box-shadow: inset 3px 0 #dc2626; }
    .annotation-p1 { background: var(--p1); box-shadow: inset 3px 0 #f97316; }
    .annotation-p2 { background: var(--p2); box-shadow: inset 3px 0 #ca8a04; }
    .annotation-language { text-decoration: underline var(--language) 2px; }
    .annotation-structure { box-shadow: inset 3px 0 var(--structure); }
    .annotation-evidence { box-shadow: inset 3px 0 var(--evidence); }
    .annotation-selected { outline: 2px solid var(--accent); outline-offset: 2px; }
    .span-highlight {
      background: #dbeafe;
      border-radius: 3px;
      padding: 0 2px;
      box-shadow: inset 0 -2px rgba(47, 111, 237, 0.28);
      cursor: pointer;
    }
    .span-highlight.annotation-language {
      text-decoration: none;
    }
    .span-highlight.annotation-selected {
      outline-offset: 1px;
    }
    .term-highlight {
      background: var(--term-bg);
      border-radius: 3px;
      box-shadow: inset 0 -1px var(--term-border);
      padding: 0 1px;
    }
    .span-highlight.term-highlight {
      background: linear-gradient(180deg, #dbeafe 0%, #dbeafe 55%, var(--term-bg) 55%, var(--term-bg) 100%);
    }
    label {
      display: block;
      font-size: 12px;
      font-weight: 700;
      color: #344054;
      margin: 12px 0 5px;
    }
    #editorPane select, #editorPane textarea, #editorPane input {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 7px;
      background: #fff;
      padding: 8px;
    }
    textarea {
      min-height: 110px;
      resize: vertical;
    }
    .target-box, .status-box, .list-box {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
      padding: 10px;
      font-size: 12px;
      color: var(--muted);
      overflow-wrap: anywhere;
    }
    .button-row {
      display: flex;
      gap: 8px;
      margin-top: 12px;
    }
    .annotation-list {
      display: grid;
      gap: 8px;
    }
    .annotation-list-empty {
      color: var(--muted);
      font-size: 12px;
    }
    .annotation-list-item {
      border: 1px solid #e4e7ec;
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
    }
    .annotation-list-item[open] {
      border-color: #bfdbfe;
    }
    .annotation-list-item.selected {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(47, 111, 237, 0.14);
    }
    .annotation-list-item summary {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      padding: 9px 10px;
      cursor: pointer;
      list-style: none;
      font-weight: 400;
    }
    .annotation-list-item summary::-webkit-details-marker {
      display: none;
    }
    .annotation-list-title {
      min-width: 0;
    }
    .annotation-list-title strong {
      color: var(--text);
      font-size: 12px;
    }
    .annotation-list-meta {
      color: var(--muted);
      font-size: 11px;
      margin-top: 2px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .annotation-list-chevron {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    .annotation-list-item[open] .annotation-list-chevron {
      transform: rotate(90deg);
    }
    .annotation-list-detail {
      border-top: 1px solid #edf2f7;
      padding: 9px 10px 10px;
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }
    .annotation-list-detail-row + .annotation-list-detail-row {
      margin-top: 7px;
    }
    .annotation-list-detail-row span {
      display: block;
      color: #344054;
      font-weight: 700;
      margin-bottom: 2px;
    }
    .term-panel {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #f8fafc;
      padding: 16px;
      align-self: start;
      position: sticky;
      top: 70px;
    }
    .term-panel h2, .term-list-panel h2 {
      font-size: 16px;
      margin: 0 0 10px;
    }
    .term-panel input, .term-panel textarea, .term-panel select {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 7px;
      background: #fff;
      padding: 8px;
      font: inherit;
    }
    .term-list-panel {
      min-width: 0;
    }
    .term-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }
    .term-source {
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }
    .term-table-wrap {
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: auto;
      background: #fff;
    }
    .term-table {
      width: 100%;
      border-collapse: collapse;
      min-width: 860px;
      font-size: 12px;
    }
    .term-table th, .term-table td {
      border-bottom: 1px solid #edf2f7;
      padding: 8px 9px;
      text-align: left;
      vertical-align: top;
    }
    .term-table th {
      background: #f8fafc;
      color: #344054;
      font-weight: 700;
      position: sticky;
      top: 0;
      z-index: 1;
    }
    .term-row.selected {
      outline: 2px solid rgba(47, 111, 237, 0.32);
      outline-offset: -2px;
      background: #eff6ff;
    }
    .term-chip {
      display: inline-block;
      margin: 0 4px 4px 0;
      padding: 1px 6px;
      border-radius: 999px;
      background: var(--term-bg);
      border: 1px solid var(--term-border);
      color: #166534;
      white-space: nowrap;
    }
    .term-empty {
      border: 1px dashed var(--border);
      border-radius: 8px;
      background: #fff;
      padding: 14px;
      color: var(--muted);
      font-size: 13px;
    }
    .error {
      border: 1px solid #fecaca;
      background: #fef2f2;
      color: #991b1b;
      padding: 12px;
      border-radius: 8px;
    }
    @media (max-width: 900px) {
      .annotation-layout, .terminology-layout { grid-template-columns: 1fr; }
      #editorPane, #savedPane { position: static; height: auto; border-left: 0; border-top: 1px solid var(--border); }
      .term-panel { position: static; }
      .virtual-list { height: 68vh; }
    }
  </style>
</head>
<body>
  <header>
    <h1>论文修复批注 / Revision Annotation</h1>
    <nav class="top-tabs" aria-label="页面 / Pages">
      <button class="top-tab active" id="annotationTab" onclick="showPage('annotation')">批注工作台 / Annotations</button>
      <button class="top-tab" id="terminologyTab" onclick="showPage('terminology')">术语清单 / Terminology</button>
    </nav>
    <div class="meta" id="headerMeta">正在加载 / Loading...</div>
    <button id="manualSave">保存 / Save</button>
  </header>
  <main id="annotationPage" class="app-page annotation-layout">
    <section id="treePane">
      <div class="toolbar">
        <label for="viewMode" style="margin:0">视图 / View</label>
        <select id="viewMode">
          <option value="full_manuscript">完整文稿 / Full manuscript</option>
          <option value="failed_or_targeted">失败/目标句 / Failed or targeted</option>
        </select>
        <span class="meta">自动保存 / Autosave on change</span>
        <span id="saveState" class="meta"></span>
      </div>
      <div id="chapterStepper" class="chapter-stepper"></div>
      <div id="treeRoot">正在加载文稿 / Loading manuscript...</div>
    </section>
    <aside id="editorPane">
      <h2 style="font-size:16px;margin:0 0 10px">批注 / Annotation</h2>
      <div id="targetBox" class="target-box">请选择文本、句子、段落、章节或插入标记 / Select text, a sentence, a paragraph, a section, or an insertion marker.</div>

      <label for="issueType">问题类型 / Problem type</label>
      <select id="issueType"></select>

      <label for="severity">严重程度 / Severity</label>
      <select id="severity">
        <option value="">未设置 / Not set</option>
        <option value="P0">P0</option>
        <option value="P1">P1</option>
        <option value="P2">P2</option>
      </select>

      <label for="suggestedAction">建议动作 / Suggested action</label>
      <select id="suggestedAction"></select>

      <label for="comment">备注（可选）/ Comment (optional)</label>
      <textarea id="comment" placeholder="可填写修改意见 / Optional user comment"></textarea>

      <div class="button-row">
        <button class="primary" id="saveAnnotation">立即保存当前批注 / Save now</button>
        <button id="clearSelection">取消选择 / Clear</button>
        <button id="clearComment">清除备注 / Clear comment</button>
        <button class="danger" id="deleteAnnotation">删除 / Delete</button>
      </div>

      <label>状态 / Status</label>
      <div id="statusBox" class="status-box">尚未选择批注 / No annotation selected.</div>
    </aside>
    <aside id="savedPane">
      <h2 style="font-size:16px;margin:0 0 10px">已保存批注 / Saved annotations</h2>
      <label>已保存批注 / Saved annotations</label>
      <div id="annotationList" class="list-box"></div>
    </aside>
  </main>
  <main id="terminologyPage" class="app-page terminology-layout" hidden>
    <section class="term-panel">
      <h2>术语编辑 / Term editor</h2>
      <input type="hidden" id="termEditIndex" value="">
      <label for="termTerm">术语 / Term</label>
      <input id="termTerm" placeholder="例如：volatile sulfur compounds">

      <label for="termLanguage">语言 / Language</label>
      <select id="termLanguage">
        <option value="">未设置 / Not set</option>
        <option value="en">English / en</option>
        <option value="zh">中文 / zh</option>
        <option value="bilingual">双语 / bilingual</option>
        <option value="symbol">符号/缩写 / symbol</option>
      </select>

      <label for="termPreferred">推荐写法 / Preferred form</label>
      <input id="termPreferred" placeholder="推荐写法，留空则使用术语本身 / Preferred form">

      <label for="termAccepted">可接受变体 / Accepted variants</label>
      <textarea id="termAccepted" placeholder="一行一个，或用逗号/分号分隔 / One per line, comma, or semicolon separated"></textarea>

      <label for="termChineseTranslations">中文译名 / Chinese translations</label>
      <textarea id="termChineseTranslations" placeholder="一行一个，例如：挥发性硫化合物 / One Chinese translation per line"></textarea>

      <label for="termField">领域 / Field or domain</label>
      <input id="termField" placeholder="例如：environmental catalysis / plasma-catalytic VSC treatment">

      <label for="termType">术语类型 / Term type</label>
      <select id="termType">
        <option value="">未设置 / Not set</option>
        <option value="professional_term">专业术语 / professional_term</option>
        <option value="proper_noun_or_named_method">专有名词/命名方法 / proper_noun_or_named_method</option>
        <option value="abbreviation">缩写 / abbreviation</option>
        <option value="chemical_species">化学物种 / chemical_species</option>
        <option value="instrument_or_method">仪器或方法 / instrument_or_method</option>
        <option value="regulation_or_standard">法规或标准 / regulation_or_standard</option>
        <option value="project_local_label">项目内标签 / project_local_label</option>
      </select>

      <label for="termSourceProvenance">来源依据 / Source provenance</label>
      <textarea id="termSourceProvenance" placeholder="一行一个：句子ID、引用文献键、材料路径或来源说明 / One source per line"></textarea>

      <label for="termForbidden">不推荐/禁用变体 / Forbidden variants</label>
      <textarea id="termForbidden" placeholder="一行一个，或用逗号/分号分隔 / One per line, comma, or semicolon separated"></textarea>

      <label for="termReason">说明 / Reason</label>
      <textarea id="termReason" placeholder="来源、定义或使用边界 / Source, definition, or scope"></textarea>

      <label><input type="checkbox" id="termConfirmed"> 已确认 / Confirmed</label>

      <div class="button-row">
        <button class="primary" id="saveTerm">保存术语 / Save term</button>
        <button id="newTerm">新建 / New</button>
        <button class="danger" id="deleteTerm">删除 / Delete</button>
      </div>
      <div id="termSaveState" class="status-box" style="margin-top:12px">术语清单未加载 / Terminology not loaded.</div>
    </section>
    <section class="term-list-panel">
      <div class="term-toolbar">
        <div>
          <h2>项目术语/专有名词清单 / Project terminology glossary</h2>
          <div id="termSource" class="term-source"></div>
        </div>
        <button id="reloadTerms">重新加载 / Reload</button>
      </div>
      <div id="termList"></div>
    </section>
  </main>
  <script>
    const PROBLEM_TYPES = __PROBLEM_TYPES__;
    const SUGGESTED_ACTIONS = __SUGGESTED_ACTIONS__;
    const DEFAULT_ACTION_BY_ISSUE = __DEFAULT_ACTION_BY_ISSUE__;
    const PROBLEM_TYPE_LABELS = {
      language_style: '语言风格 / language_style',
      grammar: '语法 / grammar',
      ambiguity: '歧义 / ambiguity',
      terminology: '术语 / terminology',
      citation_expression: '引用表达 / citation_expression',
      unsupported_claim: '缺少支撑的论断 / unsupported_claim',
      unsupported_superiority_claim: '缺少支撑的优越性论断 / unsupported_superiority_claim',
      duplicate_argument: '重复论证 / duplicate_argument',
      context_fit: '上下文衔接 / context_fit',
      paragraph_logic: '段落逻辑 / paragraph_logic',
      section_positioning: '章节定位 / section_positioning',
      needs_insert_sentence: '需要插入句子 / needs_insert_sentence',
      needs_delete: '需要删除 / needs_delete',
      needs_merge: '需要合并 / needs_merge',
      needs_split: '需要拆分 / needs_split',
      operation_record_residue: '操作记录残留 / operation_record_residue',
      figure_table_text: '图表文字 / figure_table_text',
      other: '其他 / other'
    };
    const ACTION_LABELS = {
      direct_revision_candidate: '可直接修改 / direct_revision_candidate',
      language_review_needed: '需要语言审查 / language_review_needed',
      upgrade_required: '需要升级处理 / upgrade_required',
      evidence_verification_needed: '需要证据核验 / evidence_verification_needed',
      literature_verification_needed: '需要文献核验 / literature_verification_needed',
      structure_rewrite_needed: '需要结构重写 / structure_rewrite_needed',
      final_polish_later: '稍后最终润色 / final_polish_later',
      keep_with_note: '保留并备注 / keep_with_note',
      other: '其他 / other'
    };
    const ANNOTATION_TYPE_LABELS = {
      span_issue: '文本片段问题 / span_issue',
      sentence_issue: '句子问题 / sentence_issue',
      paragraph_comment: '段落批注 / paragraph_comment',
      section_comment: '小节批注 / section_comment',
      chapter_comment: '章节批注 / chapter_comment',
      insert_between_sentences: '句间插入 / insert_between_sentences',
      figure_table_text_comment: '图表文字批注 / figure_table_text_comment'
    };
    const TARGET_LABELS = {
      paper_id: '论文 / paper_id',
      chapter_id: '章节 / chapter_id',
      section_id: '小节 / section_id',
      paragraph_id: '段落 / paragraph_id',
      sentence_id: '句子 / sentence_id',
      object_id: '对象 / object_id',
      after_sentence_id: '前一句 / after_sentence_id',
      before_sentence_id: '后一句 / before_sentence_id',
      char_start: '起始字符 / char_start',
      char_end: '结束字符 / char_end',
      ranges: '多个片段 / ranges',
      selection_scope: '选择范围 / selection_scope',
      selected_text: '选中文本 / selected_text',
      text_hash: '文本哈希 / text_hash'
    };
    const STATUS_LABELS = {
      user_commented: '用户已批注 / user_commented',
      needs_relocation: '需要重新定位 / needs_relocation'
    };
    const SENTENCE_DECISION_LABELS = {
      pass: '已通过 / Pass',
      fail: '未通过 / Fail'
    };
    let manuscript = null;
    let annotationDoc = null;
    let termDoc = {exists: false, terms: []};
    let currentAnnotation = null;
    let currentTermIndex = '';
    let saveTimer = null;
    let commentIsComposing = false;
    let activeChapterIndex = 0;
    let virtualState = {
      rows: [],
      heights: [],
      offsets: [],
      totalHeight: 0,
      activeNodeId: '',
      pendingScrollTarget: null,
      renderTimer: null,
      resizeTimer: null
    };
    const DEFAULT_ROW_HEIGHT = 220;
    const SECTION_ROW_HEIGHT = 54;
    const VIRTUAL_OVERSCAN_PX = 700;
    const VIRTUAL_ROW_GAP = 10;

    function htmlEscape(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      }[ch]));
    }

    async function fetchJSON(url, options) {
      const response = await fetch(url, options);
      const text = await response.text();
      let data = {};
      try { data = text ? JSON.parse(text) : {}; } catch (_) { data = {error: text}; }
      if (!response.ok) {
        throw new Error(data.error || response.statusText);
      }
      return data;
    }

    async function sha256(text) {
      const normalized = String(text ?? '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
      if (!window.crypto || !window.crypto.subtle) return '';
      const bytes = new TextEncoder().encode(normalized);
      const digest = await crypto.subtle.digest('SHA-256', bytes);
      return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    function splitListText(value) {
      return String(value ?? '')
        .split(/[\n,;；]+/)
        .map(item => item.trim())
        .filter(Boolean);
    }

    function uniqueStrings(values) {
      const seen = new Set();
      const out = [];
      for (const value of values || []) {
        const text = String(value ?? '').trim();
        const key = text.toLocaleLowerCase();
        if (!text || seen.has(key)) continue;
        seen.add(key);
        out.push(text);
      }
      return out;
    }

    function normalizeTermItem(item) {
      const term = String(item?.term || '').trim();
      const preferred = String(item?.preferred_form || '').trim() || term;
      return {
        term,
        language: String(item?.language || '').trim(),
        preferred_form: preferred,
        accepted_variants: uniqueStrings(Array.isArray(item?.accepted_variants) ? item.accepted_variants : splitListText(item?.accepted_variants || '')),
        chinese_translations: uniqueStrings(Array.isArray(item?.chinese_translations) ? item.chinese_translations : splitListText(item?.chinese_translations || '')),
        forbidden_variants: uniqueStrings(Array.isArray(item?.forbidden_variants) ? item.forbidden_variants : splitListText(item?.forbidden_variants || '')),
        field: String(item?.field || '').trim(),
        term_type: String(item?.term_type || '').trim(),
        source_provenance: uniqueStrings(Array.isArray(item?.source_provenance) ? item.source_provenance : splitListText(item?.source_provenance || '')),
        reason: String(item?.reason || '').trim(),
        confirmed: Boolean(item?.confirmed)
      };
    }

    function issueDefaultAction(issueType) {
      return DEFAULT_ACTION_BY_ISSUE[issueType] || 'direct_revision_candidate';
    }

    function optionLabel(labels, value) {
      return labels[value] || value;
    }

    function annotationTypeLabel(value) {
      return ANNOTATION_TYPE_LABELS[value] || value || '';
    }

    function statusLabel(value) {
      return STATUS_LABELS[value] || value || '';
    }

    function sentenceDecisionLabel(value) {
      return SENTENCE_DECISION_LABELS[value] || SENTENCE_DECISION_LABELS.fail;
    }

    function fillSelects() {
      const issue = document.getElementById('issueType');
      issue.innerHTML = PROBLEM_TYPES.map(v => `<option value="${v}">${htmlEscape(optionLabel(PROBLEM_TYPE_LABELS, v))}</option>`).join('');
      const action = document.getElementById('suggestedAction');
      action.innerHTML = SUGGESTED_ACTIONS.map(v => `<option value="${v}">${htmlEscape(optionLabel(ACTION_LABELS, v))}</option>`).join('');
    }

    async function loadAll() {
      try {
        const view = document.getElementById('viewMode').value;
        manuscript = await fetchJSON('/api/manuscript?view=' + encodeURIComponent(view));
        annotationDoc = await fetchJSON('/api/annotations');
        termDoc = await fetchJSON('/api/terminology');
        document.getElementById('headerMeta').textContent =
          `${manuscript.paper.title || '未命名文稿 / Untitled'} | ${manuscript.round} | ${manuscript.annotation_path}`;
        activeChapterIndex = Math.max(0, activeChapterIndex);
        renderTermList();
        renderTree();
        renderAnnotationList();
        setSaveState('已加载 / Loaded');
      } catch (error) {
        document.getElementById('treeRoot').innerHTML = `<div class="error">${htmlEscape(error.message)}</div>`;
        setSaveState('加载失败 / Load failed');
      }
    }

    function renderTree() {
      const root = manuscript.root || {children: manuscript.tree || []};
      const items = chapterItems(root);
      if (!items.length) {
        document.getElementById('chapterStepper').innerHTML = '';
        document.getElementById('treeRoot').innerHTML = '<div class="error">当前视图没有可显示内容 / No content is available in this view.</div>';
        return;
      }
      if (activeChapterIndex >= items.length) activeChapterIndex = 0;
      renderChapterStepper(items);
      renderVirtualChapter(items[activeChapterIndex].node);
    }

    function chapterItems(root) {
      const children = root.children || [];
      if (!children.length) return [];
      const chapters = children.filter(child => child.node_type === 'chapter');
      if (!chapters.length) {
        return [{node: {
          node_type: 'paper',
          id: root.id || 'manuscript',
          title: root.title || '全文 / Manuscript',
          children
        }, virtual: true}];
      }
      const items = chapters.map(node => ({node, virtual: false}));
      const unassigned = children.filter(child => child.node_type !== 'chapter');
      if (unassigned.length) {
        items.push({node: {
          node_type: 'chapter',
          id: '__unassigned_content',
          title: '未分章内容 / Unassigned content',
          children: unassigned
        }, virtual: true});
      }
      return items;
    }

    function countNodeType(node, type) {
      if (!node) return 0;
      let total = node.node_type === type ? 1 : 0;
      for (const child of node.children || []) total += countNodeType(child, type);
      return total;
    }

    function nodeContainsTarget(node, target) {
      if (!node || !target) return false;
      if (target.chapter_id && node.node_type === 'chapter' && node.id === target.chapter_id) return true;
      if (target.section_id && node.node_type === 'section' && node.id === target.section_id) return true;
      if (target.paragraph_id && node.node_type === 'paragraph' && node.id === target.paragraph_id) return true;
      if (target.sentence_id && node.node_type === 'sentence' && (node.sentence_id === target.sentence_id || node.id === target.sentence_id)) return true;
      if (target.after_sentence_id && node.node_type === 'sentence' && (node.sentence_id === target.after_sentence_id || node.id === target.after_sentence_id)) return true;
      if (target.before_sentence_id && node.node_type === 'sentence' && (node.sentence_id === target.before_sentence_id || node.id === target.before_sentence_id)) return true;
      if (target.object_id && (node.id === target.object_id || node.object_id === target.object_id)) return true;
      return (node.children || []).some(child => nodeContainsTarget(child, target));
    }

    function findChapterIndexForAnnotation(annotation) {
      const root = manuscript?.root || {children: manuscript?.tree || []};
      const items = chapterItems(root);
      const target = annotation?.target || {};
      return items.findIndex(item => nodeContainsTarget(item.node, target));
    }

    function renderChapterStepper(items) {
      const active = items[activeChapterIndex];
      const stepButtons = items.map((item, index) => {
        const activeClass = index === activeChapterIndex ? ' active' : '';
        const label = htmlEscape(item.node.title || item.node.id || `章节 / Chapter ${index + 1}`);
        return `<button class="step${activeClass}" title="${label}" onclick="setActiveChapter(${index})"><span class="step-index">${index + 1}</span><span class="step-label">${label}</span></button>`;
      }).join('');
      const sentenceCount = countNodeType(active.node, 'sentence');
      const paragraphCount = countNodeType(active.node, 'paragraph');
      const activeTitle = htmlEscape(active.node.title || active.node.id || '');
      document.getElementById('chapterStepper').innerHTML = `
        <div class="stepper-head">
          <strong>按章步进 / Chapter stepper</strong>
          <span class="stepper-count">${activeChapterIndex + 1}/${items.length} · ${paragraphCount} 段 / paragraphs · ${sentenceCount} 句 / sentences</span>
        </div>
        <div class="stepper-buttons">
          ${stepButtons}
        </div>
        <div class="chapter-note">当前仅渲染 / Rendering only: ${activeTitle}</div>`;
    }

    function setActiveChapter(index) {
      activeChapterIndex = index;
      renderTree();
      document.getElementById('treePane').scrollTo({top: 0, behavior: 'smooth'});
    }

    function virtualRowEstimate(row) {
      if (row.kind === 'section') return SECTION_ROW_HEIGHT;
      const textLength = collectNodeText(row.node).length;
      const sentenceCount = countNodeType(row.node, 'sentence');
      if (row.kind === 'figure_table_text') return Math.max(120, 110 + Math.ceil(textLength / 85) * 24);
      if (row.kind === 'sentence') return Math.max(120, 96 + Math.ceil(textLength / 85) * 24);
      return Math.max(150, 118 + sentenceCount * 44 + Math.ceil(textLength / 85) * 24);
    }

    function collectNodeText(node) {
      if (!node) return '';
      let text = node.text || '';
      for (const child of node.children || []) text += ' ' + collectNodeText(child);
      return text;
    }

    function flattenVirtualRows(node, context = {}) {
      if (!node) return [];
      const rows = [];
      const nodeType = node.node_type;
      const nodeId = node.id || node.chapter_id || node.section_id || node.paragraph_id || node.sentence_id || '';
      const nextContext = {...context};
      if (nodeType === 'chapter') nextContext.chapter_id = node.id || node.chapter_id || '';
      if (nodeType === 'section') {
        nextContext.section_id = node.id || node.section_id || '';
        rows.push({kind: 'section', node, context: {...nextContext}, key: `section:${nodeId}`});
      }
      if (nodeType === 'paragraph') {
        rows.push({kind: 'paragraph', node, context: {...nextContext}, key: `paragraph:${nodeId}`});
        return rows;
      }
      if (nodeType === 'sentence') {
        rows.push({kind: 'sentence', node, context: {...nextContext}, key: `sentence:${nodeId}`});
        return rows;
      }
      if (nodeType === 'figure_table_text') {
        rows.push({kind: 'figure_table_text', node, context: {...nextContext}, key: `figure:${nodeId}`});
        return rows;
      }
      for (const child of node.children || []) rows.push(...flattenVirtualRows(child, nextContext));
      return rows;
    }

    function recomputeVirtualOffsets() {
      virtualState.offsets = [];
      let offset = 0;
      for (let i = 0; i < virtualState.rows.length; i++) {
        virtualState.offsets[i] = offset;
        offset += (virtualState.heights[i] || DEFAULT_ROW_HEIGHT) + VIRTUAL_ROW_GAP;
      }
      virtualState.totalHeight = offset;
    }

    function renderVirtualChapter(node) {
      const id = htmlEscape(node.id || '');
      const title = htmlEscape(node.title || node.id || node.node_type || '');
      const rawRows = flattenVirtualRows(node);
      virtualState.rows = rawRows;
      virtualState.heights = rawRows.map(virtualRowEstimate);
      virtualState.activeNodeId = node.id || node.title || '';
      recomputeVirtualOffsets();
      const commentType = node.node_type === 'chapter' ? 'chapter_comment' : 'section_comment';
      const canComment = node.node_type === 'chapter' || node.node_type === 'section';
      const commentButton = canComment
        ? `<button class="node-comment" onclick="makeNodeAnnotation('${commentType}', '${id}')">章节批注 / Comment chapter</button>`
        : '';
      document.getElementById('treeRoot').innerHTML = `
        <article data-paper-id="${id}" ${node.node_type === 'chapter' ? `data-chapter-id="${id}"` : ''}>
          <div class="virtual-chapter-head"><h2>${title}</h2>${commentButton}</div>
          <div class="virtual-debug" id="virtualDebug"></div>
          <div class="virtual-list" id="virtualList" aria-label="章节内容 / Chapter content">
            <div class="virtual-spacer" id="virtualSpacer" style="height:${virtualState.totalHeight}px"></div>
          </div>
        </article>`;
      const list = document.getElementById('virtualList');
      list.addEventListener('scroll', scheduleVirtualRender, {passive: true});
      renderVisibleRows();
    }

    function scheduleVirtualRender() {
      if (virtualState.renderTimer) return;
      virtualState.renderTimer = requestAnimationFrame(() => {
        virtualState.renderTimer = null;
        renderVisibleRows();
      });
    }

    function visibleRowRange(scrollTop, viewportHeight) {
      const startTop = Math.max(0, scrollTop - VIRTUAL_OVERSCAN_PX);
      const endTop = scrollTop + viewportHeight + VIRTUAL_OVERSCAN_PX;
      let start = 0;
      while (
        start < virtualState.rows.length &&
        virtualState.offsets[start] + (virtualState.heights[start] || DEFAULT_ROW_HEIGHT) + VIRTUAL_ROW_GAP < startTop
      ) start += 1;
      let end = start;
      while (end < virtualState.rows.length && virtualState.offsets[end] < endTop) end += 1;
      return [Math.max(0, start), Math.min(virtualState.rows.length, end + 1)];
    }

    function renderVisibleRows() {
      const list = document.getElementById('virtualList');
      const spacer = document.getElementById('virtualSpacer');
      if (!list || !spacer) return;
      const [start, end] = visibleRowRange(list.scrollTop, list.clientHeight || 500);
      const rowsHtml = [];
      for (let index = start; index < end; index++) {
        const row = virtualState.rows[index];
        rowsHtml.push(`<div class="virtual-row" data-virtual-index="${index}" style="transform:translateY(${virtualState.offsets[index]}px)">${renderVirtualRow(row)}</div>`);
      }
      spacer.style.height = `${virtualState.totalHeight}px`;
      spacer.innerHTML = rowsHtml.join('');
      const debug = document.getElementById('virtualDebug');
      if (debug) debug.textContent = `虚拟滚动 / Virtual rows: ${start + 1}-${end} / ${virtualState.rows.length}`;
      applyAnnotationHighlights();
      measureVisibleRows();
    }

    function resetVisibleRowHeights() {
      if (!virtualState.rows.length) return;
      virtualState.heights = virtualState.rows.map(virtualRowEstimate);
      recomputeVirtualOffsets();
      renderVisibleRows();
    }

    function measureVisibleRows() {
      const spacer = document.getElementById('virtualSpacer');
      if (!spacer) return;
      let changed = false;
      spacer.querySelectorAll('.virtual-row').forEach(rowEl => {
        const index = Number(rowEl.dataset.virtualIndex || -1);
        if (index < 0) return;
        const measured = Math.ceil(Math.max(rowEl.getBoundingClientRect().height, rowEl.scrollHeight));
        if (measured > 0 && Math.abs(measured - virtualState.heights[index]) > 4) {
          virtualState.heights[index] = measured;
          changed = true;
        }
      });
      if (changed) {
        recomputeVirtualOffsets();
        spacer.style.height = `${virtualState.totalHeight}px`;
        requestAnimationFrame(renderVisibleRows);
      }
    }

    function targetSentenceId(target = {}) {
      return target.sentence_id || target.after_sentence_id || target.before_sentence_id || '';
    }

    function scrollRenderedTargetIntoView(target, block = 'center') {
      const list = document.getElementById('virtualList');
      if (!list || !target) return false;
      const sentenceId = targetSentenceId(target);
      let selector = '';
      if (sentenceId) selector = `.sentence[data-sentence-id="${CSS.escape(sentenceId)}"]`;
      else if (target.paragraph_id) selector = `.paragraph[data-paragraph-id="${CSS.escape(target.paragraph_id)}"]`;
      else if (target.object_id) selector = `.figure-text[data-figure-table-text-id="${CSS.escape(target.object_id)}"]`;
      else if (target.section_id) selector = `.virtual-section-row[data-section-id="${CSS.escape(target.section_id)}"]`;
      else if (target.chapter_id) selector = `article[data-chapter-id="${CSS.escape(target.chapter_id)}"]`;
      if (!selector) return false;
      const el = list.querySelector(selector);
      if (!el) return false;
      el.scrollIntoView({block, inline: 'nearest'});
      el.classList.add('annotation-selected');
      return true;
    }

    function refinePendingAnnotationScroll() {
      const pending = virtualState.pendingScrollTarget;
      if (!pending) return;
      const target = pending.target || {};
      const found = scrollRenderedTargetIntoView(target, pending.block || 'center');
      pending.attempts = (pending.attempts || 0) + 1;
      if (found || pending.attempts >= 8) {
        virtualState.pendingScrollTarget = null;
        return;
      }
      requestAnimationFrame(refinePendingAnnotationScroll);
    }

    function renderVirtualRow(row) {
      if (!row) return '';
      if (row.kind === 'section') return renderSectionRow(row.node, row.context);
      if (row.kind === 'paragraph') return renderParagraphNode(row.node, row.context);
      if (row.kind === 'sentence') return renderSentenceFallback(row.node, row.context);
      if (row.kind === 'figure_table_text') return renderFigureTableText(row.node, row.context);
      return '';
    }

    function renderSectionRow(n, context) {
      const id = htmlEscape(n.id || '');
      const title = htmlEscape(n.title || n.id || '');
      return `<div class="virtual-section-row" data-chapter-id="${htmlEscape(context.chapter_id || '')}" data-section-id="${id}" data-node-type="section">
        <span class="node-row"><span>${title}</span><span class="node-id">${id}</span>
        <button class="node-comment" onclick="event.preventDefault(); event.stopPropagation(); makeNodeAnnotation('section_comment', '${id}')">小节批注 / Comment section</button></span>
      </div>`;
    }

    function renderParagraphNode(n, context = {}) {
      const id = htmlEscape(n.id || n.paragraph_id || '');
      const role = n.paragraph_role || n.title || '';
      const titleText = role === 'sentence-aligned item group'
        ? '句子审阅项组 / sentence-aligned item group'
        : (n.title || n.paragraph_role || n.id || n.paragraph_id || '');
      const title = htmlEscape(titleText);
      const childContext = {...context, paragraph_id: n.id || n.paragraph_id || ''};
      const children = n.children || [];
      let body = '';
      for (let i = 0; i < children.length; i++) {
        body += renderNode(children[i], childContext);
        if (children[i].node_type === 'sentence' && i < children.length - 1 && children[i + 1].node_type === 'sentence') {
          body += `<button class="gap-button" title="在此插入批注 / Insert comment here" onclick="makeInsertAnnotation('${htmlEscape(children[i].sentence_id)}', '${htmlEscape(children[i + 1].sentence_id)}')">+</button>`;
        }
      }
      return `<div class="paragraph" data-chapter-id="${htmlEscape(context.chapter_id || '')}" data-section-id="${htmlEscape(context.section_id || '')}" data-paragraph-id="${id}">
        <div class="paragraph-head"><span>${title} <span class="node-id">${id}</span></span>
        <button class="node-comment" onclick="makeNodeAnnotation('paragraph_comment', '${id}')">段落批注 / Comment paragraph</button></div>
        <div>${body}</div>
      </div>`;
    }

    function renderSentenceFallback(n, context = {}) {
      const id = htmlEscape(n.id || n.sentence_id || '');
      return `<div class="paragraph" data-chapter-id="${htmlEscape(context.chapter_id || '')}" data-section-id="${htmlEscape(context.section_id || '')}">
        ${renderNode(n, context)}
      </div>`;
    }

    function renderFigureTableText(n, context = {}) {
      const id = htmlEscape(n.id || n.object_id || '');
      const title = htmlEscape(n.title || n.type || n.id || n.object_id || '');
      const rawText = normalizeUiText(n.text || '');
      return `<div class="figure-text" data-chapter-id="${htmlEscape(context.chapter_id || '')}" data-section-id="${htmlEscape(context.section_id || '')}" data-figure-table-text-id="${id}">
        <div class="paragraph-head"><span>${title} <span class="node-id">${id}</span></span>
        <button class="node-comment" onclick="makeNodeAnnotation('figure_table_text_comment', '${id}')">批注 / Comment</button></div>
        ${renderBilingualText(rawText, [], terminologyRanges(rawText))}
      </div>`;
    }

    function rowMatchesTarget(row, target) {
      if (!row || !target) return false;
      const node = row.node || {};
      const context = row.context || {};
      const sentenceIds = new Set([target.sentence_id, target.after_sentence_id, target.before_sentence_id].filter(Boolean));
      if (sentenceIds.size) {
        if (row.kind === 'sentence') return sentenceIds.has(node.sentence_id || node.id);
        return (node.children || []).some(child => sentenceIds.has(child.sentence_id || child.id));
      }
      if (target.paragraph_id && (node.id === target.paragraph_id || node.paragraph_id === target.paragraph_id)) return true;
      if (target.object_id && (node.id === target.object_id || node.object_id === target.object_id)) return true;
      if (target.section_id) return row.kind === 'section' && (node.id === target.section_id || node.section_id === target.section_id);
      if (target.chapter_id) return row.kind === 'section' && context.chapter_id === target.chapter_id;
      return false;
    }

    function scrollToAnnotationTarget(annotation) {
      const target = annotation?.target || {};
      const list = document.getElementById('virtualList');
      if (!list || !virtualState.rows.length) return;
      const index = virtualState.rows.findIndex(row => rowMatchesTarget(row, target));
      if (index < 0) return;
      list.scrollTop = Math.max(0, (virtualState.offsets[index] || 0) - 70);
      renderVisibleRows();
      virtualState.pendingScrollTarget = {target, attempts: 0, block: 'center'};
      requestAnimationFrame(refinePendingAnnotationScroll);
    }

    function hasHan(text) {
      return /[\u3400-\u9fff]/.test(text);
    }

    function hasLatin(text) {
      return /[A-Za-z]/.test(text);
    }

    function normalizeUiText(text) {
      return String(text ?? '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
    }

    function splitBilingualParts(text) {
      const normalized = String(text ?? '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
      if (!normalized) return [];
      const explicitParts = [];
      for (const match of normalized.matchAll(/[^\n]+/g)) {
        const rawLine = match[0];
        const leading = rawLine.search(/\S/);
        const trimmed = rawLine.trim();
        if (trimmed) explicitParts.push({text: trimmed, start: match.index + Math.max(leading, 0)});
      }
      if (explicitParts.length > 1) return explicitParts;
      if (!hasHan(normalized) || !hasLatin(normalized)) return [{text: normalized, start: 0}];

      const candidates = [];
      for (const match of normalized.matchAll(/\s+/g)) {
        const beforeRaw = normalized.slice(0, match.index);
        const afterRaw = normalized.slice(match.index + match[0].length);
        const before = beforeRaw.trim();
        const after = afterRaw.trim();
        if (before && after && hasHan(before) && hasLatin(after) && (/^[A-Za-z(]/.test(after) || after.startsWith('['))) {
          const score = /[。！？；：:]$/.test(before) ? 2 : 1;
          const beforeLeading = beforeRaw.search(/\S/);
          const afterLeading = afterRaw.search(/\S/);
          candidates.push({
            parts: [
              {text: before, start: Math.max(beforeLeading, 0)},
              {text: after, start: match.index + match[0].length + Math.max(afterLeading, 0)}
            ],
            score
          });
        }
      }
      candidates.sort((a, b) => b.score - a.score);
      return candidates.length ? candidates[0].parts : [{text: normalized, start: 0}];
    }

    function spanTargetRanges(annotation) {
      const target = annotation?.target || {};
      if (Array.isArray(target.ranges) && target.ranges.length) {
        return target.ranges.filter(item => item && typeof item === 'object');
      }
      return [target];
    }

    function resolveSpanRangeFromTarget(rangeTarget, rawText) {
      let start = Number(rangeTarget.char_start);
      let end = Number(rangeTarget.char_end);
      if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) return null;
      const selectedText = normalizeUiText(rangeTarget.selected_text || '');
      const rangedText = normalizeUiText(rawText.slice(start, end));
      if (selectedText && rangedText !== selectedText) {
        return null;
      }
      return {start, end};
    }

    function spanRangesForAnnotation(annotation, rawText) {
      return spanTargetRanges(annotation)
        .map((rangeTarget, rangeIndex) => {
          const range = resolveSpanRangeFromTarget(rangeTarget, rawText);
          return range ? {annotation, rangeIndex, ...range} : null;
        })
        .filter(Boolean);
    }

    function sentenceSpanAnnotations(sentenceId, rawText) {
      return (annotationDoc?.annotations || [])
        .filter(annotation => {
          const target = annotation.target || {};
          return annotation.annotation_type === 'span_issue'
            && target.sentence_id === sentenceId;
        })
        .flatMap(annotation => spanRangesForAnnotation(annotation, rawText))
        .sort((a, b) => a.start - b.start || a.end - b.end);
    }

    function termSearchValues() {
      if (!termDoc?.exists) return [];
      const values = [];
      for (const item of termDoc.terms || []) {
        const term = normalizeTermItem(item);
        values.push(term.term, term.preferred_form, ...term.accepted_variants, ...term.chinese_translations);
      }
      return uniqueStrings(values).filter(value => value.length >= 2).sort((a, b) => b.length - a.length || a.localeCompare(b));
    }

    function isWordChar(ch) {
      return /[A-Za-z0-9_+-]/.test(ch || '');
    }

    function termBoundaryOk(rawText, start, end, value) {
      if (hasHan(value)) return true;
      return !isWordChar(rawText[start - 1]) && !isWordChar(rawText[end]);
    }

    function terminologyRanges(rawText) {
      if (!termDoc?.exists || !(termDoc.terms || []).length) return [];
      const ranges = [];
      const lower = rawText.toLocaleLowerCase();
      const occupied = [];
      for (const value of termSearchValues()) {
        const needle = value.toLocaleLowerCase();
        let index = lower.indexOf(needle);
        while (index >= 0) {
          const end = index + value.length;
          const overlaps = occupied.some(range => index < range.end && end > range.start);
          if (!overlaps && termBoundaryOk(rawText, index, end, value)) {
            ranges.push({start: index, end, term: value});
            occupied.push({start: index, end});
          }
          index = lower.indexOf(needle, index + Math.max(1, needle.length));
        }
      }
      return ranges.sort((a, b) => a.start - b.start || a.end - b.end);
    }

    function latexFormulaRanges(partText) {
      const ranges = [];
      const pattern = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|\$[^$\n]+\$)/g;
      for (const match of partText.matchAll(pattern)) {
        const raw = match[0];
        const block = raw.startsWith('$$') || raw.startsWith('\\[');
        ranges.push({
          start: match.index,
          end: match.index + raw.length,
          text: raw,
          block
        });
      }
      return ranges;
    }

    function renderFormulaAwareText(part, spanAnnotations = [], termAnnotations = []) {
      const formulas = latexFormulaRanges(part.text);
      if (!formulas.length) return renderTextWithHighlights(part, spanAnnotations, termAnnotations);
      let cursor = 0;
      const out = [];
      for (const formula of formulas) {
        if (formula.start > cursor) {
          out.push(renderTextWithHighlights({
            text: part.text.slice(cursor, formula.start),
            start: (part.start || 0) + cursor
          }, spanAnnotations, termAnnotations));
        }
        const formulaPart = {
          text: formula.text,
          start: (part.start || 0) + formula.start
        };
        const rendered = renderTextWithHighlights(formulaPart, spanAnnotations, termAnnotations);
        const klass = formula.block ? 'formula-block' : 'formula-inline';
        out.push(`<code class="${klass}" title="LaTeX source">${rendered}</code>`);
        cursor = formula.end;
      }
      if (cursor < part.text.length) {
        out.push(renderTextWithHighlights({
          text: part.text.slice(cursor),
          start: (part.start || 0) + cursor
        }, spanAnnotations, termAnnotations));
      }
      return out.join('');
    }

    function renderTextWithHighlights(part, spanAnnotations = [], termAnnotations = []) {
      const partStart = part.start || 0;
      const partEnd = partStart + part.text.length;
      const clippedSpans = spanAnnotations
        .map(item => ({...item, start: Math.max(partStart, item.start), end: Math.min(partEnd, item.end)}))
        .filter(item => item.end > item.start);
      const clippedTerms = termAnnotations
        .map(item => ({...item, start: Math.max(partStart, item.start), end: Math.min(partEnd, item.end)}))
        .filter(item => item.end > item.start);
      if (!clippedSpans.length && !clippedTerms.length) return htmlEscape(part.text);
      const boundaries = new Set([partStart, partEnd]);
      for (const item of [...clippedSpans, ...clippedTerms]) {
        boundaries.add(item.start);
        boundaries.add(item.end);
      }
      const points = Array.from(boundaries).sort((a, b) => a - b);
      const pieces = [];
      for (let i = 0; i < points.length - 1; i++) {
        const start = points[i];
        const end = points[i + 1];
        if (end <= start) continue;
        const activeSpans = clippedSpans.filter(item => item.start < end && item.end > start);
        const activeTerms = clippedTerms.filter(item => item.start < end && item.end > start);
        pieces.push({text: part.text.slice(start - partStart, end - partStart), activeSpans, activeTerms});
      }
      return pieces.map(piece => {
        if (!piece.activeSpans.length && !piece.activeTerms.length) return htmlEscape(piece.text);
        const selected = piece.activeSpans.find(item => currentAnnotation?.annotation_id && currentAnnotation.annotation_id === item.annotation.annotation_id)
          || piece.activeSpans.slice().sort((a, b) => (a.end - a.start) - (b.end - b.start))[0];
        const classes = [];
        if (piece.activeTerms.length) classes.push('term-highlight');
        if (piece.activeSpans.length) {
          classes.push('span-highlight');
          for (const item of piece.activeSpans) classes.push(...annotationClasses(item.annotation));
          if (piece.activeSpans.some(item => currentAnnotation?.annotation_id && currentAnnotation.annotation_id === item.annotation.annotation_id)) {
            classes.push('annotation-selected');
          }
        }
        const uniqueClasses = Array.from(new Set(classes));
        const ids = piece.activeSpans.map(item => item.annotation.annotation_id).filter(Boolean);
        const termTitle = piece.activeTerms.map(item => item.term).filter(Boolean).join(' | ');
        const title = ids.map(id => {
          const annotation = piece.activeSpans.find(item => item.annotation.annotation_id === id)?.annotation;
          return `${id} ${optionLabel(PROBLEM_TYPE_LABELS, annotation?.issue_type || '')}`.trim();
        }).join(' | ');
        const fullTitle = [termTitle ? `术语 / Term: ${termTitle}` : '', title].filter(Boolean).join(' | ');
        if (selected) {
          return `<mark class="${uniqueClasses.join(' ')}" data-span-annotation-id="${htmlEscape(selected.annotation.annotation_id || '')}" data-span-annotation-ids="${htmlEscape(ids.join(' '))}" title="${htmlEscape(fullTitle)}" onclick="spanHighlightClicked(event)">${htmlEscape(piece.text)}</mark>`;
        }
        return `<mark class="${uniqueClasses.join(' ')}" title="${htmlEscape(fullTitle)}">${htmlEscape(piece.text)}</mark>`;
      }).join('');
    }

    function spanHighlightClicked(event) {
      const selection = window.getSelection();
      if (selection && selection.toString().trim()) return;
      event.preventDefault();
      event.stopPropagation();
      const id = event.currentTarget?.dataset?.spanAnnotationId || '';
      if (id) selectAnnotation(id);
    }

    function renderBilingualText(text, spanAnnotations = [], termAnnotations = []) {
      const parts = splitBilingualParts(text);
      if (!parts.length) return '';
      return parts.map(part => {
        const klass = hasLatin(part.text) && !hasHan(part.text) ? 'sentence-line english' : 'sentence-line';
        return `<span class="${klass}" data-part-start="${part.start}">${renderFormulaAwareText(part, spanAnnotations, termAnnotations)}</span>`;
      }).join('');
    }

    function sentenceDecision(sentenceId) {
      const decision = annotationDoc?.sentence_status_decisions?.[sentenceId];
      if (typeof decision === 'string') return decision;
      if (decision && typeof decision === 'object') return decision.status || '';
      return '';
    }

    function sentenceEffectiveStatus(n) {
      const sentenceId = n.sentence_id || n.id || '';
      const status = sentenceDecision(sentenceId) || 'fail';
      return status === 'pass' ? 'pass' : 'fail';
    }

    function renderSentenceStatusControls(n) {
      const sentenceId = htmlEscape(n.sentence_id || n.id || '');
      const normalized = sentenceEffectiveStatus(n);
      return `<div class="sentence-tools" onclick="event.stopPropagation()">
        <span class="sentence-status-badge ${normalized}">${sentenceDecisionLabel(normalized)}</span>
        <button class="status-toggle ${normalized === 'pass' ? 'active pass' : ''}" title="标记为通过 / Mark as pass" onclick="setSentenceStatus('${sentenceId}', 'pass', event)">通过 / Pass</button>
        <button class="status-toggle ${normalized === 'fail' ? 'active fail' : ''}" title="标记为未通过 / Mark as fail" onclick="setSentenceStatus('${sentenceId}', 'fail', event)">未通过 / Fail</button>
      </div>`;
    }

    function renderNode(n, context = {}) {
      if (!n) return '';
      const id = htmlEscape(n.id || '');
      const title = htmlEscape(n.title || n.id || n.node_type);
      if (n.node_type === 'paper') {
        return `<article data-paper-id="${id}"><h2>${title}</h2>${(n.children || []).map(child => renderNode(child, context)).join('')}</article>`;
      }
      if (n.node_type === 'chapter' || n.node_type === 'section') {
        const nextContext = {...context};
        if (n.node_type === 'chapter') nextContext.chapter_id = n.id || n.chapter_id || '';
        if (n.node_type === 'section') nextContext.section_id = n.id || n.section_id || '';
        const attr = n.node_type === 'chapter' ? 'data-chapter-id' : 'data-section-id';
        const commentType = n.node_type === 'chapter' ? 'chapter_comment' : 'section_comment';
        return `<details open ${attr}="${id}" data-node-type="${n.node_type}">
          <summary><span class="node-row"><span>${title}</span><span class="node-id">${id}</span>
          <button class="node-comment" onclick="event.preventDefault(); event.stopPropagation(); makeNodeAnnotation('${commentType}', '${id}')">批注 / Comment</button></span></summary>
          ${(n.children || []).map(child => renderNode(child, nextContext)).join('')}
        </details>`;
      }
      if (n.node_type === 'paragraph') {
        return renderParagraphNode(n, context);
      }
      if (n.node_type === 'sentence') {
        const sid = htmlEscape(n.sentence_id || n.id);
        const rawText = normalizeUiText(n.text || '');
        const rawTextAttr = htmlEscape(rawText).replace(/\n/g, '&#10;');
        const spanAnnotations = sentenceSpanAnnotations(n.sentence_id || n.id, rawText);
        const termAnnotations = terminologyRanges(rawText);
        return `<div class="sentence" data-chapter-id="${htmlEscape(context.chapter_id || '')}" data-section-id="${htmlEscape(context.section_id || '')}" data-sentence-id="${sid}" data-paragraph-id="${htmlEscape(n.paragraph_id || context.paragraph_id || '')}" data-hash="${htmlEscape(n.hash || '')}" data-text="${rawTextAttr}" onclick="sentenceClicked(event, '${sid}')">${renderSentenceStatusControls(n)}${renderBilingualText(rawText, spanAnnotations, termAnnotations)}</div>`;
      }
      if (n.node_type === 'figure_table_text') {
        return renderFigureTableText(n, context);
      }
      return '';
    }

    function annotationClasses(annotation) {
      const classes = [];
      if (annotation.severity) classes.push('annotation-' + String(annotation.severity).toLowerCase());
      if (annotation.suggested_action === 'upgrade_required' || annotation.issue_type === 'unsupported_claim' || annotation.issue_type === 'unsupported_superiority_claim') classes.push('annotation-evidence');
      if (annotation.issue_type === 'paragraph_logic' || annotation.issue_type === 'section_positioning') classes.push('annotation-structure');
      if (annotation.issue_type === 'language_style' || annotation.issue_type === 'grammar' || annotation.issue_type === 'ambiguity') classes.push('annotation-language');
      return classes;
    }

    function applyAnnotationHighlights() {
      document.querySelectorAll('.annotation-p0,.annotation-p1,.annotation-p2,.annotation-evidence,.annotation-structure,.annotation-language,.annotation-selected')
        .forEach(el => el.classList.remove('annotation-p0','annotation-p1','annotation-p2','annotation-evidence','annotation-structure','annotation-language','annotation-selected'));
      for (const annotation of annotationDoc.annotations || []) {
        const t = annotation.target || {};
        const classes = annotationClasses(annotation);
        let selector = '';
        if (annotation.annotation_type === 'span_issue' && t.sentence_id && spanTargetRanges(annotation).length) {
          selector = annotation.annotation_id
            ? `[data-span-annotation-id="${CSS.escape(annotation.annotation_id)}"], [data-span-annotation-ids~="${CSS.escape(annotation.annotation_id)}"]`
            : '';
        } else if (annotation.annotation_type === 'paragraph_comment' && t.paragraph_id) {
          selector = `.paragraph[data-paragraph-id="${CSS.escape(t.paragraph_id)}"]`;
        } else if (annotation.annotation_type === 'section_comment' && t.section_id) {
          selector = `.virtual-section-row[data-section-id="${CSS.escape(t.section_id)}"], details[data-section-id="${CSS.escape(t.section_id)}"]`;
        } else if (annotation.annotation_type === 'chapter_comment' && t.chapter_id) {
          selector = `article[data-chapter-id="${CSS.escape(t.chapter_id)}"], details[data-chapter-id="${CSS.escape(t.chapter_id)}"]`;
        } else if (t.sentence_id) selector = `.sentence[data-sentence-id="${CSS.escape(t.sentence_id)}"]`;
        else if (t.paragraph_id) selector = `.paragraph[data-paragraph-id="${CSS.escape(t.paragraph_id)}"]`;
        else if (t.section_id) selector = `.virtual-section-row[data-section-id="${CSS.escape(t.section_id)}"], details[data-section-id="${CSS.escape(t.section_id)}"]`;
        else if (t.chapter_id) selector = `article[data-chapter-id="${CSS.escape(t.chapter_id)}"], details[data-chapter-id="${CSS.escape(t.chapter_id)}"]`;
        if (selector) {
          document.querySelectorAll(selector).forEach(el => {
            el.classList.add(...classes);
            if (currentAnnotation?.annotation_id && currentAnnotation.annotation_id === annotation.annotation_id) {
              el.classList.add('annotation-selected');
            }
          });
        }
      }
    }

    function refreshCurrentViewHighlights() {
      if (document.getElementById('virtualList')) renderVisibleRows();
      else applyAnnotationHighlights();
    }

    function closestFromNode(node, selector) {
      if (!node) return null;
      const el = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
      return el ? el.closest(selector) : null;
    }

    function textOffsetInElement(element, container, offset) {
      const range = document.createRange();
      range.selectNodeContents(element);
      try {
        range.setEnd(container, offset);
        return range.toString().length;
      } catch (_) {
        return 0;
      }
    }

    function sentenceCharOffset(sentenceEl, container, offset) {
      const line = closestFromNode(container, '.sentence-line');
      if (line && sentenceEl.contains(line)) {
        return Number(line.dataset.partStart || 0) + textOffsetInElement(line, container, offset);
      }
      if (container === sentenceEl && sentenceEl.childNodes.length) {
        const lines = Array.from(sentenceEl.querySelectorAll('.sentence-line'));
        if (lines.length) {
          if (offset <= 0) return Number(lines[0].dataset.partStart || 0);
          const lineIndex = Math.min(offset - 1, lines.length - 1);
          const selectedLine = lines[lineIndex];
          return Number(selectedLine.dataset.partStart || 0) + selectedLine.textContent.length;
        }
      }
      return textOffsetInElement(sentenceEl, container, offset);
    }

    function sentenceClicked(event, sentenceId) {
      const selection = window.getSelection();
      if (selection && selection.toString().trim()) return;
      const sentenceEl = event.currentTarget;
      const paragraphEl = sentenceEl.closest('[data-paragraph-id]');
      const sectionEl = sentenceEl.closest('[data-section-id]');
      const chapterEl = sentenceEl.closest('[data-chapter-id]');
      const annotation = baseAnnotation('sentence_issue');
      annotation.target = {
        chapter_id: chapterEl?.dataset.chapterId || '',
        section_id: sectionEl?.dataset.sectionId || '',
        paragraph_id: paragraphEl?.dataset.paragraphId || '',
        sentence_id: sentenceId,
        text_hash: sentenceEl.dataset.hash || ''
      };
      showAnnotation(annotation, true);
    }

    async function captureSelection() {
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      const selectedText = selection.toString();
      if (!selectedText.trim()) return;
      const range = selection.getRangeAt(0);
      const startSentence = closestFromNode(range.startContainer, '[data-sentence-id]');
      const endSentence = closestFromNode(range.endContainer, '[data-sentence-id]');
      if (!startSentence || !endSentence || startSentence.dataset.sentenceId !== endSentence.dataset.sentenceId) {
        setSaveState('选区必须位于同一句内 / Selection must stay within one sentence');
        return;
      }
      let charStart = sentenceCharOffset(startSentence, range.startContainer, range.startOffset);
      let charEnd = sentenceCharOffset(startSentence, range.endContainer, range.endOffset);
      if (charEnd < charStart) [charStart, charEnd] = [charEnd, charStart];
      const rawSentenceText = startSentence.dataset.text || '';
      const selectedRawText = rawSentenceText && charEnd > charStart
        ? rawSentenceText.slice(charStart, charEnd).trim()
        : selectedText.trim();
      const wholeSentence = rawSentenceText && charStart === 0 && charEnd === rawSentenceText.length;
      const paragraphEl = startSentence.closest('[data-paragraph-id]');
      const sectionEl = startSentence.closest('[data-section-id]');
      const chapterEl = startSentence.closest('[data-chapter-id]');
      const annotation = baseAnnotation('span_issue');
      annotation.target = {
        chapter_id: chapterEl?.dataset.chapterId || '',
        section_id: sectionEl?.dataset.sectionId || '',
        paragraph_id: paragraphEl?.dataset.paragraphId || '',
        sentence_id: startSentence.dataset.sentenceId,
        char_start: charStart,
        char_end: charEnd,
        selection_scope: wholeSentence ? 'whole_sentence' : 'text_span',
        selected_text: selectedRawText,
        text_hash: await sha256(selectedRawText)
      };
      showAnnotation(annotation, true);
    }

    function baseAnnotation(annotationType) {
      const issueType = annotationType === 'insert_between_sentences' ? 'needs_insert_sentence' : 'language_style';
      return {
        annotation_type: annotationType,
        target: {},
        issue_type: issueType,
        severity: '',
        suggested_action: issueDefaultAction(issueType),
        comment: '',
        status: 'user_commented'
      };
    }

    function makeNodeAnnotation(type, id) {
      const annotation = baseAnnotation(type);
      if (type === 'paragraph_comment') annotation.target = {paragraph_id: id};
      else if (type === 'section_comment') {
        annotation.target = {section_id: id};
        annotation.issue_type = 'section_positioning';
        annotation.suggested_action = issueDefaultAction(annotation.issue_type);
      } else if (type === 'chapter_comment') {
        annotation.target = {chapter_id: id};
        annotation.issue_type = 'section_positioning';
        annotation.suggested_action = issueDefaultAction(annotation.issue_type);
      } else {
        annotation.target = {object_id: id};
        annotation.issue_type = 'figure_table_text';
      }
      showAnnotation(annotation, true);
    }

    function makeInsertAnnotation(afterId, beforeId) {
      const annotation = baseAnnotation('insert_between_sentences');
      annotation.target = {after_sentence_id: afterId, before_sentence_id: beforeId};
      showAnnotation(annotation, true);
    }

    function formatTargetValue(key, value) {
      if (key === 'ranges' && Array.isArray(value)) {
        return `${value.length} 个片段 / ranges\n` + value.map((range, index) => {
          const start = range?.char_start ?? '';
          const end = range?.char_end ?? '';
          const text = range?.selected_text ? `: ${range.selected_text}` : '';
          return `  ${index + 1}. ${start}-${end}${text}`;
        }).join('\n');
      }
      if (value && typeof value === 'object') return JSON.stringify(value);
      return String(value);
    }

    function targetSummary(annotation) {
      const target = annotation?.target || {};
      return Object.entries(target)
        .filter(([, v]) => v !== '')
        .map(([k, v]) => `${TARGET_LABELS[k] || k}: ${formatTargetValue(k, v)}`)
        .join('\n') || '暂无目标 / No target';
    }

    function showAnnotation(annotation, autosave, options = {}) {
      currentAnnotation = structuredClone(annotation);
      document.getElementById('issueType').value = currentAnnotation.issue_type || 'language_style';
      document.getElementById('severity').value = currentAnnotation.severity || '';
      document.getElementById('suggestedAction').value = currentAnnotation.suggested_action || issueDefaultAction(currentAnnotation.issue_type);
      const preserveCommentDraft = options.preserveCommentDraft || commentIsComposing;
      if (!preserveCommentDraft) {
        document.getElementById('comment').value = currentAnnotation.comment || '';
      }
      document.getElementById('targetBox').textContent = targetSummary(currentAnnotation);
      document.getElementById('statusBox').textContent = `${currentAnnotation.annotation_id || '新建 / new'} | ${annotationTypeLabel(currentAnnotation.annotation_type)} | ${statusLabel(currentAnnotation.status || 'user_commented')}`;
      refreshCurrentViewHighlights();
      if (autosave) scheduleSaveCurrent();
    }

    function updateCurrentFromPanel() {
      if (!currentAnnotation) return;
      currentAnnotation.issue_type = document.getElementById('issueType').value;
      currentAnnotation.severity = document.getElementById('severity').value;
      currentAnnotation.suggested_action = document.getElementById('suggestedAction').value || issueDefaultAction(currentAnnotation.issue_type);
      currentAnnotation.comment = document.getElementById('comment').value;
      currentAnnotation.status = 'user_commented';
    }

    function clearCommentText(autosave = true) {
      clearTimeout(saveTimer);
      commentIsComposing = false;
      document.getElementById('comment').value = '';
      if (currentAnnotation) {
        updateCurrentFromPanel();
        currentAnnotation.comment = '';
        if (autosave) scheduleSaveCurrent();
      }
      if (autosave) setSaveState('备注已清除 / Comment cleared');
    }

    function resetCurrentAnnotationPanel() {
      currentAnnotation = null;
      clearTimeout(saveTimer);
      document.getElementById('comment').value = '';
      document.getElementById('targetBox').textContent = '请选择文本、句子、段落、章节或插入标记 / Select text, a sentence, a paragraph, a section, or an insertion marker.';
      document.getElementById('statusBox').textContent = '尚未选择批注 / No annotation selected.';
    }

    function currentAnnotationIdAfterSave(result) {
      if (!currentAnnotation) return '';
      const oldId = currentAnnotation.annotation_id || '';
      const idMap = result?.annotation_id_map || {};
      return idMap[oldId] || oldId || result?.last_saved_annotation_id || '';
    }

    function syncCurrentAnnotationAfterSave(result) {
      const targetId = currentAnnotationIdAfterSave(result);
      if (!targetId) return;
      const saved = (result.annotations || []).find(a => a.annotation_id === targetId);
      if (saved) {
        currentAnnotation = structuredClone(saved);
        document.getElementById('statusBox').textContent = `${currentAnnotation.annotation_id || '新建 / new'} | ${annotationTypeLabel(currentAnnotation.annotation_type)} | ${statusLabel(currentAnnotation.status || 'user_commented')}`;
      } else {
        resetCurrentAnnotationPanel();
      }
    }

    function annotationTargetsSentence(annotation, sentenceId) {
      const target = annotation?.target || {};
      return Boolean(sentenceId && target.sentence_id === sentenceId);
    }

    function markAnnotatedSentenceFailed(annotation) {
      const sentenceId = annotation?.target?.sentence_id || '';
      if (!sentenceId || !annotationDoc) return false;
      annotationDoc.sentence_status_decisions = annotationDoc.sentence_status_decisions || {};
      const decision = annotationDoc.sentence_status_decisions[sentenceId];
      const status = typeof decision === 'string' ? decision : decision?.status;
      if (status !== 'pass') return false;
      annotationDoc.sentence_status_decisions[sentenceId] = {
        status: 'fail',
        updated_at: new Date().toISOString()
      };
      return true;
    }

    function appendResolvedAnnotations(sentenceId, removedAnnotations) {
      if (!removedAnnotations.length || annotationDoc?.modification_log_exists) return;
      annotationDoc.resolved_annotations = Array.isArray(annotationDoc.resolved_annotations) ? annotationDoc.resolved_annotations : [];
      const stamp = new Date().toISOString();
      for (const annotation of removedAnnotations) {
        annotationDoc.resolved_annotations.push({
          resolved_at: stamp,
          resolution: 'sentence_marked_pass',
          sentence_id: sentenceId,
          annotation: structuredClone(annotation),
          note: 'UI-only resolution record because no formal modification_log.md entry was found when the sentence was marked pass.'
        });
      }
    }

    function removeAnnotationsForPassedSentence(sentenceId) {
      const annotations = annotationDoc?.annotations || [];
      const removed = annotations.filter(annotation => annotationTargetsSentence(annotation, sentenceId));
      if (!removed.length) return [];
      appendResolvedAnnotations(sentenceId, removed);
      annotationDoc.annotations = annotations.filter(annotation => !annotationTargetsSentence(annotation, sentenceId));
      if (currentAnnotation && annotationTargetsSentence(currentAnnotation, sentenceId)) {
        resetCurrentAnnotationPanel();
      }
      return removed;
    }

    function scheduleSaveCurrent() {
      if (commentIsComposing) return;
      clearTimeout(saveTimer);
      saveTimer = setTimeout(() => saveCurrent(), 450);
    }

    async function saveCurrent() {
      if (!currentAnnotation) return;
      if (commentIsComposing) {
        setSaveState('中文输入中，稍后自动保存 / IME composition in progress');
        return;
      }
      updateCurrentFromPanel();
      if (!currentAnnotation.issue_type) {
        setSaveState('必须选择问题类型 / Problem type is required');
        return;
      }
      const changedPassToFail = markAnnotatedSentenceFailed(currentAnnotation);
      if (changedPassToFail) refreshCurrentViewHighlights();
      try {
        const result = await fetchJSON('/api/annotations', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({annotation: currentAnnotation})
        });
        annotationDoc = result;
        syncCurrentAnnotationAfterSave(result);
        renderAnnotationList();
        refreshCurrentViewHighlights();
        setSaveState(changedPassToFail
          ? '已保存；该句新增批注后已自动改为未通过 / Saved; annotated sentence changed to fail'
          : '已保存 / Saved');
      } catch (error) {
        setSaveState('保存失败 / Save failed: ' + error.message);
      }
    }

    function clearCurrentSelection() {
      resetCurrentAnnotationPanel();
      renderAnnotationList();
      setSaveState('已取消选择 / Selection cleared');
      refreshCurrentViewHighlights();
    }

    async function deleteCurrent() {
      if (!currentAnnotation || !currentAnnotation.annotation_id) return;
      try {
        annotationDoc = await fetchJSON('/api/annotations/delete', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({annotation_id: currentAnnotation.annotation_id})
        });
        currentAnnotation = null;
        resetCurrentAnnotationPanel();
        renderAnnotationList();
        refreshCurrentViewHighlights();
        setSaveState('已删除 / Deleted');
      } catch (error) {
        setSaveState('删除失败 / Delete failed: ' + error.message);
      }
    }

    async function manualSave() {
      try {
        annotationDoc = await fetchJSON('/api/save', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(annotationDoc || {})
        });
        syncCurrentAnnotationAfterSave(annotationDoc);
        renderAnnotationList();
        refreshCurrentViewHighlights();
        setSaveState('已保存 / Saved');
      } catch (error) {
        setSaveState('保存失败 / Save failed: ' + error.message);
      }
    }

    async function setSentenceStatus(sentenceId, status, event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      if (!annotationDoc) return;
      annotationDoc.sentence_status_decisions = annotationDoc.sentence_status_decisions || {};
      const normalized = status === 'pass' ? 'pass' : 'fail';
      annotationDoc.sentence_status_decisions[sentenceId] = {
        status: normalized,
        updated_at: new Date().toISOString()
      };
      const removedAnnotations = normalized === 'pass' ? removeAnnotationsForPassedSentence(sentenceId) : [];
      if (removedAnnotations.length) renderAnnotationList();
      refreshCurrentViewHighlights();
      try {
        annotationDoc = await fetchJSON('/api/save', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(annotationDoc || {})
        });
        syncCurrentAnnotationAfterSave(annotationDoc);
        renderAnnotationList();
        refreshCurrentViewHighlights();
        const removedText = removedAnnotations.length ? `；已移除 ${removedAnnotations.length} 条同句批注 / removed ${removedAnnotations.length} annotation(s)` : '';
        setSaveState(`句子状态已保存：${sentenceDecisionLabel(normalized)}${removedText} / Saved`);
      } catch (error) {
        setSaveState('句子状态保存失败 / Status save failed: ' + error.message);
      }
    }

    function showPage(pageName) {
      const terminology = pageName === 'terminology';
      document.getElementById('annotationPage').hidden = terminology;
      document.getElementById('terminologyPage').hidden = !terminology;
      document.getElementById('annotationTab').classList.toggle('active', !terminology);
      document.getElementById('terminologyTab').classList.toggle('active', terminology);
      if (terminology) renderTermList();
    }

    function termFormValue() {
      return normalizeTermItem({
        term: document.getElementById('termTerm').value,
        language: document.getElementById('termLanguage').value,
        preferred_form: document.getElementById('termPreferred').value,
        accepted_variants: splitListText(document.getElementById('termAccepted').value),
        chinese_translations: splitListText(document.getElementById('termChineseTranslations').value),
        forbidden_variants: splitListText(document.getElementById('termForbidden').value),
        field: document.getElementById('termField').value,
        term_type: document.getElementById('termType').value,
        source_provenance: splitListText(document.getElementById('termSourceProvenance').value),
        reason: document.getElementById('termReason').value,
        confirmed: document.getElementById('termConfirmed').checked
      });
    }

    function setTermForm(item = null, index = '') {
      const term = item ? normalizeTermItem(item) : normalizeTermItem({});
      currentTermIndex = index === '' ? '' : String(index);
      document.getElementById('termEditIndex').value = currentTermIndex;
      document.getElementById('termTerm').value = term.term;
      document.getElementById('termLanguage').value = term.language;
      document.getElementById('termPreferred').value = term.preferred_form && term.preferred_form !== term.term ? term.preferred_form : '';
      document.getElementById('termAccepted').value = term.accepted_variants.join('\n');
      document.getElementById('termChineseTranslations').value = term.chinese_translations.join('\n');
      document.getElementById('termForbidden').value = term.forbidden_variants.join('\n');
      document.getElementById('termField').value = term.field;
      document.getElementById('termType').value = term.term_type;
      document.getElementById('termSourceProvenance').value = term.source_provenance.join('\n');
      document.getElementById('termReason').value = term.reason;
      document.getElementById('termConfirmed').checked = term.confirmed;
      document.getElementById('termSaveState').textContent = currentTermIndex === '' ? '新建术语 / New term' : `正在编辑第 ${Number(currentTermIndex) + 1} 条 / Editing term ${Number(currentTermIndex) + 1}`;
      renderTermList();
    }

    function renderTermChips(values) {
      const items = uniqueStrings(values || []);
      if (!items.length) return '<span class="meta">-</span>';
      return items.map(value => `<span class="term-chip">${htmlEscape(value)}</span>`).join('');
    }

    function renderTermList() {
      const source = document.getElementById('termSource');
      const list = document.getElementById('termList');
      if (!source || !list) return;
      const terms = (termDoc?.terms || []).map(normalizeTermItem);
      source.textContent = termDoc?.exists
        ? `来源 / Source: ${termDoc.source_path || 'shared/terminology_glossary.yaml'} · ${terms.length} 条 / terms`
        : '未找到 shared/terminology_glossary.yaml；正文不渲染术语底色。保存术语后会创建清单。 / No glossary found; term highlighting is disabled until saved.';
      if (!terms.length) {
        list.innerHTML = '<div class="term-empty">暂无术语。可在左侧新建术语，保存后会写入 shared/terminology_glossary.yaml 和 terminology_glossary.md。 / No terms yet.</div>';
        return;
      }
      list.innerHTML = `<div class="term-table-wrap"><table class="term-table">
        <thead><tr>
          <th>术语 / Term</th><th>推荐写法 / Preferred</th><th>领域 / Field</th><th>类型 / Type</th><th>中文译名 / Chinese</th><th>变体 / Variants</th><th>来源 / Source</th><th>状态 / Status</th><th>操作 / Action</th>
        </tr></thead>
        <tbody>${terms.map((term, index) => `
          <tr class="term-row${String(index) === String(currentTermIndex) ? ' selected' : ''}">
            <td><strong>${htmlEscape(term.term)}</strong><br><span class="term-source">${htmlEscape(term.reason || '')}</span></td>
            <td>${htmlEscape(term.preferred_form || term.term)}</td>
            <td>${htmlEscape(term.field || '-')}<br><span class="term-source">${htmlEscape(term.language || '-')}</span></td>
            <td>${htmlEscape(term.term_type || '-')}</td>
            <td>${renderTermChips(term.chinese_translations)}</td>
            <td>${renderTermChips(term.accepted_variants)}${term.forbidden_variants.length ? '<br><span class="term-source">Forbidden:</span> ' + renderTermChips(term.forbidden_variants) : ''}</td>
            <td>${renderTermChips(term.source_provenance)}</td>
            <td>${term.confirmed ? '已确认 / Confirmed' : '未确认 / Unconfirmed'}</td>
            <td><button onclick="selectTerm(${index})">编辑 / Edit</button></td>
          </tr>`).join('')}
        </tbody></table></div>`;
    }

    function selectTerm(index) {
      const term = (termDoc?.terms || [])[index];
      if (!term) return;
      setTermForm(term, index);
    }

    async function reloadTerms() {
      try {
        termDoc = await fetchJSON('/api/terminology');
        renderTermList();
        resetVisibleRowHeights();
        document.getElementById('termSaveState').textContent = '已重新加载术语清单 / Reloaded terminology glossary';
      } catch (error) {
        document.getElementById('termSaveState').textContent = '术语清单加载失败 / Load failed: ' + error.message;
      }
    }

    async function saveTerm() {
      const term = termFormValue();
      if (!term.term) {
        document.getElementById('termSaveState').textContent = '术语不能为空 / Term is required';
        return;
      }
      const terms = (termDoc?.terms || []).map(normalizeTermItem);
      const index = currentTermIndex === '' ? -1 : Number(currentTermIndex);
      if (index >= 0 && index < terms.length) terms[index] = term;
      else terms.push(term);
      try {
        termDoc = await fetchJSON('/api/terminology', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({terms})
        });
        const savedIndex = (termDoc.terms || []).findIndex(item => normalizeTermItem(item).term === term.term);
        currentTermIndex = savedIndex >= 0 ? String(savedIndex) : '';
        renderTermList();
        resetVisibleRowHeights();
        document.getElementById('termSaveState').textContent = '术语已保存 / Term saved';
      } catch (error) {
        document.getElementById('termSaveState').textContent = '术语保存失败 / Save failed: ' + error.message;
      }
    }

    async function deleteTerm() {
      const index = currentTermIndex === '' ? -1 : Number(currentTermIndex);
      if (index < 0) return;
      const terms = (termDoc?.terms || []).map(normalizeTermItem).filter((_, itemIndex) => itemIndex !== index);
      try {
        termDoc = await fetchJSON('/api/terminology', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({terms})
        });
        setTermForm(null, '');
        resetVisibleRowHeights();
        document.getElementById('termSaveState').textContent = '术语已删除 / Term deleted';
      } catch (error) {
        document.getElementById('termSaveState').textContent = '术语删除失败 / Delete failed: ' + error.message;
      }
    }

    function renderAnnotationList() {
      const list = document.getElementById('annotationList');
      const annotations = annotationDoc?.annotations || [];
      if (!annotations.length) {
        list.innerHTML = '<div class="annotation-list-empty">暂无批注 / No annotations yet.</div>';
        return;
      }
      const selectedId = currentAnnotation?.annotation_id || '';
      list.innerHTML = `<div class="annotation-list">${annotations.map((a, index) => {
        const id = a.annotation_id || '';
        const selected = selectedId && selectedId === id;
        const issue = optionLabel(PROBLEM_TYPE_LABELS, a.issue_type);
        const type = annotationTypeLabel(a.annotation_type);
        const target = targetSummary(a);
        const comment = String(a.comment || '').trim() || '无备注 / No comment';
        const status = statusLabel(a.status || 'user_commented');
        const action = optionLabel(ACTION_LABELS, a.suggested_action || '');
        const displayNumber = `批注 ${index + 1} / #${index + 1}`;
        return `<details class="annotation-list-item${selected ? ' selected' : ''}" data-annotation-id="${htmlEscape(id)}" ${selected ? 'open' : ''}>
          <summary onclick="selectAnnotation('${htmlEscape(id)}')">
            <span class="annotation-list-title">
              <strong>${htmlEscape(displayNumber)} · ${htmlEscape(id)} ${htmlEscape(issue)}</strong>
              <span class="annotation-list-meta">${htmlEscape(type)}</span>
            </span>
            <span class="annotation-list-chevron">›</span>
          </summary>
          <div class="annotation-list-detail">
            <div class="annotation-list-detail-row"><span>目标 / Target</span>${htmlEscape(target).replace(/\n/g, '<br>')}</div>
            <div class="annotation-list-detail-row"><span>建议动作 / Suggested action</span>${htmlEscape(action || '未设置 / Not set')}</div>
            <div class="annotation-list-detail-row"><span>状态 / Status</span>${htmlEscape(status)}</div>
            <div class="annotation-list-detail-row"><span>备注 / Comment</span>${htmlEscape(comment).replace(/\n/g, '<br>')}</div>
          </div>
        </details>`;
      }).join('')}</div>`;
    }

    function selectAnnotation(id) {
      const annotation = (annotationDoc.annotations || []).find(a => a.annotation_id === id);
      if (!annotation) return;
      const targetChapterIndex = findChapterIndexForAnnotation(annotation);
      if (targetChapterIndex >= 0 && targetChapterIndex !== activeChapterIndex) {
        activeChapterIndex = targetChapterIndex;
        renderTree();
      }
      showAnnotation(annotation, false);
      scrollToAnnotationTarget(annotation);
      setTimeout(() => refinePendingAnnotationScroll(), 0);
      renderAnnotationList();
    }

    function setSaveState(text) {
      document.getElementById('saveState').textContent = text;
    }

    document.addEventListener('mouseup', () => setTimeout(captureSelection, 0));
    window.addEventListener('resize', () => {
      clearTimeout(virtualState.resizeTimer);
      virtualState.resizeTimer = setTimeout(resetVisibleRowHeights, 120);
    });
    document.getElementById('viewMode').addEventListener('change', () => {
      activeChapterIndex = 0;
      loadAll();
    });
    document.getElementById('saveAnnotation').addEventListener('click', saveCurrent);
    document.getElementById('clearSelection').addEventListener('click', clearCurrentSelection);
    document.getElementById('clearComment').addEventListener('click', () => clearCommentText(true));
    document.getElementById('deleteAnnotation').addEventListener('click', deleteCurrent);
    document.getElementById('manualSave').addEventListener('click', manualSave);
    document.getElementById('saveTerm').addEventListener('click', saveTerm);
    document.getElementById('newTerm').addEventListener('click', () => setTermForm(null, ''));
    document.getElementById('deleteTerm').addEventListener('click', deleteTerm);
    document.getElementById('reloadTerms').addEventListener('click', reloadTerms);
    for (const id of ['issueType', 'severity', 'suggestedAction', 'comment']) {
      const field = document.getElementById(id);
      field.addEventListener('input', event => {
        if (id === 'comment' && (event.isComposing || commentIsComposing)) return;
        if (id === 'issueType') {
          const issue = document.getElementById('issueType').value;
          document.getElementById('suggestedAction').value = issueDefaultAction(issue);
        }
        scheduleSaveCurrent();
      });
    }
    const commentField = document.getElementById('comment');
    commentField.addEventListener('compositionstart', () => {
      commentIsComposing = true;
      clearTimeout(saveTimer);
    });
    commentField.addEventListener('compositionend', () => {
      commentIsComposing = false;
      scheduleSaveCurrent();
    });

    fillSelects();
    loadAll();
  </script>
</body>
</html>
"""


class AnnotationHandler(BaseHTTPRequestHandler):
    state: AppState

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{self.client_address[0]} - {fmt % args}", file=sys.stderr)

    def send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text: str, content_type: str = "text/html; charset=utf-8", status: int = 200) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("request body must be a JSON object")
        return data

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/":
                page = HTML_PAGE.replace("__PROBLEM_TYPES__", json.dumps(PROBLEM_TYPES))
                page = page.replace("__SUGGESTED_ACTIONS__", json.dumps(SUGGESTED_ACTIONS))
                page = page.replace("__DEFAULT_ACTION_BY_ISSUE__", json.dumps(DEFAULT_ACTION_BY_ISSUE))
                self.send_text(page)
                return
            if parsed.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            if parsed.path == "/api/manuscript":
                self.handle_get_manuscript(parse_qs(parsed.query))
                return
            if parsed.path == "/api/annotations":
                payload = self.state.load_annotations()
                self.send_json(self.state.decorate_annotation_document(payload))
                return
            if parsed.path == "/api/terminology":
                self.send_json(self.state.load_terminology_glossary())
                return
            self.send_json({"error": "not found"}, status=404)
        except Exception as exc:  # noqa: BLE001
            self.send_json({"error": str(exc)}, status=500)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/annotations":
                self.handle_post_annotation()
                return
            if parsed.path == "/api/annotations/delete":
                self.handle_delete_annotation()
                return
            if parsed.path == "/api/save":
                document = self.read_json() or self.state.load_annotations()
                self.send_json(self.state.save_annotations(document))
                return
            if parsed.path == "/api/terminology":
                self.handle_save_terminology()
                return
            self.send_json({"error": "not found"}, status=404)
        except FileNotFoundError as exc:
            self.send_json({"error": str(exc)}, status=409)
        except Exception as exc:  # noqa: BLE001
            self.send_json({"error": str(exc)}, status=500)

    def handle_get_manuscript(self, query: dict[str, list[str]]) -> None:
        data = self.state.read_object_library()
        root, paper = normalize_tree(data)
        view = (query.get("view") or ["full_manuscript"])[0]
        failed_ids = sorted(self.state.failed_sentence_ids_for_tree(root))
        active_root = root
        if view == "failed_or_targeted":
            active_root = filter_tree_for_sentences(root, set(failed_ids)) or dict(root, children=[])
        self.send_json(
            {
                "paper": paper,
                "root": active_root,
                "tree": active_root.get("children", []),
                "round": self.state.round_id,
                "view_mode": view,
                "available_views": ["full_manuscript", "failed_or_targeted"],
                "failed_sentence_ids": failed_ids,
                "round_dir_exists": self.state.round_dir.exists(),
                "annotation_path": self.state.annotation_path.as_posix(),
                "source_object_library": self.state.source_object_library(),
            }
        )

    def handle_post_annotation(self) -> None:
        request = self.read_json()
        annotation = request.get("annotation", request)
        if not isinstance(annotation, dict):
            raise ValueError("annotation must be a JSON object")
        if not annotation.get("issue_type"):
            raise ValueError("issue_type is required")
        annotation.setdefault("annotation_type", "sentence_issue")
        annotation.setdefault("target", {})
        annotation.setdefault("suggested_action", DEFAULT_ACTION_BY_ISSUE.get(annotation["issue_type"], "direct_revision_candidate"))
        annotation.setdefault("comment", "")
        annotation.setdefault("status", "user_commented")
        document = self.state.load_annotations()
        if not annotation.get("annotation_id"):
            annotation["annotation_id"] = next_annotation_id(document)
        annotations = document.setdefault("annotations", [])
        replaced = False
        for index, existing in enumerate(annotations):
            if existing.get("annotation_id") == annotation["annotation_id"]:
                annotations[index] = annotation
                replaced = True
                break
        if not replaced:
            annotations.append(annotation)
        document["last_saved_annotation_id"] = annotation["annotation_id"]
        self.send_json(self.state.save_annotations(document))

    def handle_save_terminology(self) -> None:
        request = self.read_json()
        terms = request.get("terms", [])
        if not isinstance(terms, list):
            raise ValueError("terms must be a list")
        clean_terms = [term for term in terms if isinstance(term, dict)]
        self.send_json(self.state.save_terminology_glossary(clean_terms))

    def handle_delete_annotation(self) -> None:
        request = self.read_json()
        annotation_id = str(request.get("annotation_id", ""))
        if not annotation_id:
            raise ValueError("annotation_id is required")
        document = self.state.load_annotations()
        document["annotations"] = [
            item for item in document.get("annotations", []) if item.get("annotation_id") != annotation_id
        ]
        self.send_json(self.state.save_annotations(document))


class ReusableThreadingTCPServer(ThreadingTCPServer):
    allow_reuse_address = True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the revision annotation UI.")
    parser.add_argument("--workbench", required=True, type=Path, help="Path to revision_workbench")
    parser.add_argument("--round", default="round_001", dest="round_id", help="Round id, default: round_001")
    parser.add_argument("--host", default="127.0.0.1", help="Host, default: 127.0.0.1")
    parser.add_argument("--port", default=8765, type=int, help="Port, default: 8765")
    parser.add_argument("--create-round", action="store_true", help="Create the round directory if it is missing")
    parser.add_argument("--open", action="store_true", help="Open the UI in the default browser")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    state = AppState(args.workbench, args.round_id, args.create_round)
    AnnotationHandler.state = state
    if not state.object_path.exists():
        print(f"warning: object library not found: {state.object_path}", file=sys.stderr)
    if args.create_round:
        state.round_dir.mkdir(parents=True, exist_ok=True)
    url = f"http://{args.host}:{args.port}"
    with ReusableThreadingTCPServer((args.host, args.port), AnnotationHandler) as server:
        print(f"Revision annotation UI: {url}")
        print(f"Workbench: {state.workbench}")
        print(f"Annotation file: {state.annotation_path}")
        if args.open:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping revision annotation UI.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
