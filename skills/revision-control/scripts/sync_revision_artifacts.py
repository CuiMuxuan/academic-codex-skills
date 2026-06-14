#!/usr/bin/env python3
"""Synchronize revision-control derived artifacts from manuscript_objects.json.

This utility is the public revision-control sync entry point. It keeps the
object-library summary, full latest bilingual review, partial failed/targeted
review, shared UI resources, and terminology schema aligned with the current
object library and round annotation file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ensure_revision_ui_resources as ui_resources  # noqa: E402


DEFAULT_FIELD = "environmental catalysis / plasma-catalytic treatment of volatile sulfur compounds"


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    tmp.replace(path)


def markdown_escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def yaml_quote(value: Any) -> str:
    return json.dumps(str(value or ""), ensure_ascii=False)


def scalar_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    return [part.strip() for part in re.split(r"[\n,;；]+", str(value)) if part.strip()]


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
    return [term for term in terms if str(term.get("term", "")).strip()]


def first_value(item: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = item.get(key)
        if value is not None and str(value) != "":
            return str(value)
    return default


def paper_and_objects(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    paper = data.get("paper", data)
    if not isinstance(paper, dict):
        raise ValueError("object library must contain a paper object")
    objects = paper.get("objects", {})
    if not isinstance(objects, dict):
        raise ValueError("paper.objects must be a JSON object")
    return paper, objects


def object_items(objects: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = objects.get(key, [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def sentence_id(sentence: dict[str, Any]) -> str:
    return first_value(sentence, "sentence_id", "id")


def sentence_text(sentence: dict[str, Any]) -> str:
    return first_value(sentence, "latest_text", "text", "original_text")


def sentence_english(sentence: dict[str, Any]) -> str:
    english = first_value(sentence, "english_text")
    if english:
        return english
    text = sentence_text(sentence)
    match = re.search(r"English:\s*(.*?)(?:\n\s*中文审阅稿:|$)", text, flags=re.S)
    return match.group(1).strip() if match else text.strip()


def sentence_chinese(sentence: dict[str, Any]) -> str:
    chinese = first_value(sentence, "chinese_review_text", "chinese_text")
    if chinese:
        return chinese
    text = sentence_text(sentence)
    match = re.search(r"中文审阅稿:\s*(.*)$", text, flags=re.S)
    return match.group(1).strip() if match else ""


def normalize_status(value: Any) -> str:
    return "pass" if str(value or "").strip().lower() == "pass" else "fail"


def load_annotations(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"annotations": [], "sentence_status_decisions": {}}
    data = read_json(path)
    annotations = data.get("annotations", [])
    if not isinstance(annotations, list):
        data["annotations"] = []
    decisions = data.get("sentence_status_decisions", {})
    normalized: dict[str, dict[str, Any]] = {}
    if isinstance(decisions, dict):
        for sid, raw in decisions.items():
            if not sid:
                continue
            if isinstance(raw, dict):
                item = dict(raw)
                item["status"] = normalize_status(item.get("status"))
            else:
                item = {"status": normalize_status(raw)}
            normalized[str(sid)] = item
    data["sentence_status_decisions"] = normalized
    return data


def user_status(sentence: dict[str, Any], decisions: dict[str, dict[str, Any]]) -> str:
    sid = sentence_id(sentence)
    decision = decisions.get(sid, {})
    if decision:
        return normalize_status(decision.get("status"))
    persisted = sentence.get("user_confirmed_status") or sentence.get("confirmed_status")
    if persisted:
        return normalize_status(persisted)
    return "unconfirmed"


def suggested_status(sentence: dict[str, Any]) -> str:
    raw = sentence.get("suggested_status") or sentence.get("status") or "fail"
    return normalize_status(raw)


def section_titles(objects: dict[str, Any]) -> dict[str, str]:
    return {
        first_value(section, "section_id", "id"): first_value(section, "title", "name")
        for section in object_items(objects, "sections")
    }


def paragraph_locations(objects: dict[str, Any]) -> dict[str, str]:
    sections = section_titles(objects)
    locations: dict[str, str] = {}
    for paragraph in object_items(objects, "paragraphs"):
        pid = first_value(paragraph, "paragraph_id", "id")
        section_title = sections.get(first_value(paragraph, "section_id"), "")
        para_index = first_value(paragraph, "source_paragraph_index", "paragraph_index", default=pid)
        locations[pid] = f"{section_title} / Paragraph {para_index}".strip(" /")
    return locations


def render_manuscript_summary(paper: dict[str, Any], objects: dict[str, Any]) -> str:
    lines = [
        "# Manuscript Object Library Summary",
        "",
        f"Generated at: {now_iso()}",
        f"Paper id: `{first_value(paper, 'paper_id', 'id')}`",
        f"Title: {first_value(paper, 'title', 'name')}",
        f"Current round: `{first_value(paper, 'current_round')}`",
        f"Paragraph source mode: `{first_value(paper, 'paragraph_source_mode')}`",
        "",
        "| object type | count |",
        "|---|---:|",
    ]
    for key, label in (
        ("chapters", "chapters"),
        ("sections", "sections"),
        ("paragraphs", "paragraphs"),
        ("sentences", "sentences"),
        ("figure_table_text_objects", "figure/table text objects"),
    ):
        lines.append(f"| {label} | {len(object_items(objects, key))} |")
    lines.extend(["", "## Chapters", ""])
    for chapter in object_items(objects, "chapters"):
        lines.append(f"- `{first_value(chapter, 'chapter_id', 'id')}` {first_value(chapter, 'title', 'name')}")
    lines.append("")
    return "\n".join(lines)


def render_full_review(
    paper: dict[str, Any],
    objects: dict[str, Any],
    decisions: dict[str, dict[str, Any]],
    round_id: str,
) -> str:
    title_by_section = section_titles(objects)
    current_section = None
    lines = [
        "# Full Bilingual Sentence Review",
        "",
        "## Metadata",
        "",
        f"- manuscript: {first_value(paper, 'title', 'name')}",
        f"- round: {round_id}",
        "- version: latest",
        f"- generated_at: {now_iso()}",
        f"- source_file: {first_value(paper, 'source_manuscript_path', 'source_manuscript')}",
        "",
    ]
    for sentence in object_items(objects, "sentences"):
        section_id = first_value(sentence, "section_id")
        section_title = title_by_section.get(section_id, section_id or "Unsectioned")
        if section_title != current_section:
            lines.extend([f"## {section_title}", ""])
            current_section = section_title
        sid = sentence_id(sentence)
        lines.extend(
            [
                f"### {sid}",
                "",
                f"- Section item: {first_value(sentence, 'section_item', 'source_sentence_index')}",
                f"- Kind: {first_value(sentence, 'kind', default='prose')}",
                f"- English: {sentence_english(sentence)}",
                f"- 中文审阅稿: {sentence_chinese(sentence)}",
                f"- Suggested status: {suggested_status(sentence)}",
                f"- User confirmed status: {user_status(sentence, decisions)}",
                f"- Revision count: {first_value(sentence, 'revision_count', default='0')}",
                "",
            ]
        )
    return "\n".join(lines)


def annotation_sentence_ids(annotations: list[Any]) -> set[str]:
    ids: set[str] = set()
    for annotation in annotations:
        if not isinstance(annotation, dict):
            continue
        target = annotation.get("target", {})
        if not isinstance(target, dict):
            continue
        for key in ("sentence_id", "after_sentence_id", "before_sentence_id"):
            value = target.get(key)
            if value:
                ids.add(str(value))
    return ids


def annotation_index(annotations: list[Any]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for annotation in annotations:
        if not isinstance(annotation, dict):
            continue
        target = annotation.get("target", {})
        if not isinstance(target, dict):
            continue
        for sid in [target.get("sentence_id"), target.get("after_sentence_id"), target.get("before_sentence_id")]:
            if sid:
                index.setdefault(str(sid), []).append(annotation)
    return index


def target_text(annotation: dict[str, Any]) -> str:
    target = annotation.get("target", {}) if isinstance(annotation, dict) else {}
    if not isinstance(target, dict):
        return ""
    if target.get("selected_text"):
        return str(target["selected_text"])
    ranges = target.get("ranges")
    if isinstance(ranges, list):
        pieces = [str(item.get("selected_text", "")) for item in ranges if isinstance(item, dict) and item.get("selected_text")]
        return "; ".join(pieces)
    return ""


def render_partial_review(
    paper: dict[str, Any],
    objects: dict[str, Any],
    annotations_doc: dict[str, Any],
    round_id: str,
) -> str:
    sentences = object_items(objects, "sentences")
    by_id = {sentence_id(sentence): sentence for sentence in sentences}
    locations = paragraph_locations(objects)
    annotations = annotations_doc.get("annotations", [])
    if not isinstance(annotations, list):
        annotations = []
    decisions = annotations_doc.get("sentence_status_decisions", {})
    if not isinstance(decisions, dict):
        decisions = {}
    explicit_fail = {sid for sid, decision in decisions.items() if normalize_status(decision.get("status")) == "fail"}
    requested = annotation_sentence_ids(annotations)
    target_ids = sorted((explicit_fail | requested) & set(by_id.keys()), key=lambda sid: list(by_id.keys()).index(sid))
    ann_by_sentence = annotation_index(annotations)
    lines = [
        "# Partial Failed Sentence Review",
        "",
        "## Metadata",
        "",
        f"- manuscript: {first_value(paper, 'title', 'name')}",
        f"- round: {round_id}",
        "- target_scope: UI annotations and user-confirmed failed sentences",
        f"- generated_at: {now_iso()}",
        "",
        "## Failed Or Requested Sentences",
        "",
        "| sentence_id | location | latest_text | failure_reason | user_instruction | proposed_action | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for sid in target_ids:
        sentence = by_id[sid]
        row_annotations = ann_by_sentence.get(sid, [])
        reasons = []
        comments = []
        actions = []
        for annotation in row_annotations:
            aid = first_value(annotation, "annotation_id")
            issue = first_value(annotation, "issue_type")
            selected = target_text(annotation)
            label = f"{aid}: {issue}" if aid else issue
            if selected:
                label += f" [{selected}]"
            if label.strip():
                reasons.append(label)
            comment = first_value(annotation, "comment")
            if comment or aid:
                comments.append(f"{aid}: {comment}".strip(": "))
            action = first_value(annotation, "suggested_action")
            if action:
                actions.append(action)
        status = "fail" if sid in explicit_fail else "user_requested"
        proposed = "; ".join(dict.fromkeys(actions)) or "review_required"
        text = f"{sid} | English: {sentence_english(sentence)}<br>中文审阅稿: {sentence_chinese(sentence)}"
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape_cell(sid),
                    markdown_escape_cell(locations.get(first_value(sentence, "paragraph_id"), "")),
                    markdown_escape_cell(text),
                    markdown_escape_cell("; ".join(reasons)),
                    markdown_escape_cell("; ".join(comments)),
                    markdown_escape_cell(proposed),
                    markdown_escape_cell(status),
                ]
            )
            + " |"
        )
    chapter_items = [
        item for item in annotations if isinstance(item, dict) and item.get("annotation_type") in {"chapter_comment", "section_comment"}
    ]
    if chapter_items:
        lines.extend(["", "## Chapter-Level Items", ""])
        for item in chapter_items:
            target = item.get("target", {}) if isinstance(item.get("target", {}), dict) else {}
            owner = target.get("chapter_id") or target.get("section_id") or target.get("object_id") or ""
            lines.append(
                f"- {first_value(item, 'annotation_id')}: {owner} / {first_value(item, 'issue_type')} / {first_value(item, 'comment')}"
            )
    lines.append("")
    return "\n".join(lines)


def parse_project_field(workbench: Path) -> str:
    standards = workbench / "shared" / "project_review_standards.yaml"
    if not standards.exists():
        return DEFAULT_FIELD
    text = standards.read_text(encoding="utf-8-sig", errors="replace")
    match = re.search(r"research_field:\s*['\"]?([^'\"\n#]+)", text)
    value = match.group(1).strip() if match else ""
    return value or DEFAULT_FIELD


def classify_term_type(item: dict[str, Any]) -> str:
    term = str(item.get("term", "")).strip()
    if item.get("term_type"):
        return str(item["term_type"]).strip()
    if re.fullmatch(r"[A-Z][A-Z0-9-]{1,}", term):
        return "abbreviation"
    if re.search(r"\d|[A-Z][a-z]*[A-Z]|\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", term):
        return "proper_noun_or_named_method"
    return "professional_term"


def infer_source_provenance(item: dict[str, Any], term_context: dict[str, list[str]]) -> list[str]:
    existing = scalar_list(item.get("source_provenance", []))
    if existing:
        return existing
    term = str(item.get("term", "")).strip().lower()
    locations = term_context.get(term, [])
    if locations:
        return locations[:5]
    return ["auto-generated from manuscript object library; source sentence not uniquely located"]


def normalize_term_record(item: dict[str, Any], project_field: str, term_context: dict[str, list[str]]) -> dict[str, Any]:
    normalized = {
        "term": str(item.get("term", "")).strip(),
        "language": str(item.get("language", "")).strip(),
        "preferred_form": str(item.get("preferred_form", "")).strip() or str(item.get("term", "")).strip(),
        "accepted_variants": scalar_list(item.get("accepted_variants", [])),
        "chinese_translations": scalar_list(item.get("chinese_translations", [])),
        "forbidden_variants": scalar_list(item.get("forbidden_variants", [])),
        "field": str(item.get("field", "")).strip() or project_field,
        "term_type": classify_term_type(item),
        "source_provenance": infer_source_provenance(item, term_context),
        "reason": str(item.get("reason", "")).strip(),
        "confirmed": bool(item.get("confirmed", False)),
    }
    if not normalized["reason"]:
        normalized["reason"] = (
            "Project-specific terminology candidate. Field/domain and source provenance are required "
            "so terminology highlighting does not import unrelated disciplinary jargon."
        )
    return normalized


def build_term_context(objects: dict[str, Any]) -> dict[str, list[str]]:
    context: dict[str, list[str]] = {}
    for sentence in object_items(objects, "sentences"):
        sid = sentence_id(sentence)
        haystack = f"{sentence_english(sentence)}\n{sentence_chinese(sentence)}".lower()
        citations = "; ".join(re.findall(r"\[@([^\]]+)\]", haystack))
        location = sid if not citations else f"{sid}; citations: {citations}"
        tokens = set(re.findall(r"[A-Za-z][A-Za-z0-9-]{1,}(?:\s+[A-Za-z][A-Za-z0-9-]{1,}){0,4}", haystack))
        tokens.update(re.findall(r"[\u4e00-\u9fffA-Za-z0-9/-]{2,24}", haystack))
        for token in tokens:
            key = token.strip().lower()
            if key:
                context.setdefault(key, []).append(location)
    return context


def terminology_yaml(terms: list[dict[str, Any]]) -> str:
    lines = ["terminology_glossary:"]
    if not terms:
        return "terminology_glossary: []\n"
    for item in terms:
        lines.append(f"  - term: {yaml_quote(item['term'])}")
        lines.append(f"    language: {yaml_quote(item.get('language', ''))}")
        lines.append(f"    preferred_form: {yaml_quote(item.get('preferred_form', item['term']))}")
        for key in ("accepted_variants", "chinese_translations", "forbidden_variants", "source_provenance"):
            values = scalar_list(item.get(key, []))
            if values:
                lines.append(f"    {key}:")
                for value in values:
                    lines.append(f"      - {yaml_quote(value)}")
            else:
                lines.append(f"    {key}: []")
        lines.append(f"    field: {yaml_quote(item.get('field', ''))}")
        lines.append(f"    term_type: {yaml_quote(item.get('term_type', ''))}")
        lines.append(f"    reason: {yaml_quote(item.get('reason', ''))}")
        lines.append(f"    confirmed: {str(bool(item.get('confirmed', False))).lower()}")
    return "\n".join(lines) + "\n"


def terminology_md(terms: list[dict[str, Any]]) -> str:
    lines = [
        "# Terminology Glossary",
        "",
        "This glossary is project-specific. Auto-generated entries are candidates, not confirmed standards.",
        "Every term should record its field/domain and source provenance before it is treated as a durable project standard.",
        "",
        "| term | language | preferred form | accepted variants | Chinese translations | field | term type | source provenance | forbidden variants | confirmed | reason |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for item in terms:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape_cell(item.get("term", "")),
                    markdown_escape_cell(item.get("language", "")),
                    markdown_escape_cell(item.get("preferred_form", "")),
                    markdown_escape_cell(", ".join(item.get("accepted_variants", []) or [])),
                    markdown_escape_cell(", ".join(item.get("chinese_translations", []) or [])),
                    markdown_escape_cell(item.get("field", "")),
                    markdown_escape_cell(item.get("term_type", "")),
                    markdown_escape_cell("; ".join(item.get("source_provenance", []) or [])),
                    markdown_escape_cell(", ".join(item.get("forbidden_variants", []) or [])),
                    "yes" if item.get("confirmed") else "no",
                    markdown_escape_cell(item.get("reason", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def sync_terminology(workbench: Path, objects: dict[str, Any], check_only: bool) -> tuple[dict[str, Any], list[str]]:
    yaml_path = workbench / "shared" / "terminology_glossary.yaml"
    md_path = workbench / "shared" / "terminology_glossary.md"
    if not yaml_path.exists():
        return {"total": 0, "missing_field": 0, "missing_source_provenance": 0}, []
    terms = parse_terminology_yaml(yaml_path.read_text(encoding="utf-8-sig", errors="replace"))
    original_summary = {
        "total": len(terms),
        "missing_field": sum(1 for term in terms if not str(term.get("field", "")).strip()),
        "missing_source_provenance": sum(1 for term in terms if not scalar_list(term.get("source_provenance", []))),
    }
    project_field = parse_project_field(workbench)
    context = build_term_context(objects)
    normalized = [normalize_term_record(term, project_field, context) for term in terms]
    summary = dict(original_summary)
    summary["after_sync_missing_field"] = sum(1 for term in normalized if not term.get("field"))
    summary["after_sync_missing_source_provenance"] = sum(
        1 for term in normalized if not term.get("source_provenance")
    )
    written: list[str] = []
    if not check_only:
        write_text(yaml_path, terminology_yaml(normalized))
        write_text(md_path, terminology_md(normalized))
        written.extend([yaml_path.as_posix(), md_path.as_posix()])
    return summary, written


def update_manifest(workbench: Path, paper: dict[str, Any], round_id: str, check_only: bool) -> list[str]:
    path = workbench / "bilingual_revision" / "manifest.yaml"
    lines = [
        f"paper_id: {first_value(paper, 'paper_id', 'id')}",
        "revision_mode: bilingual_main_manuscript_paragraphs",
        f"current_round: {round_id}",
        f"source_manuscript: {first_value(paper, 'source_manuscript_path', 'source_manuscript')}",
        f"alignment_review_source: {first_value(paper, 'alignment_review_source_path')}",
        f"paragraph_source_mode: {first_value(paper, 'paragraph_source_mode')}",
        "object_library: bilingual_revision/manuscript_objects.json",
        f"annotation_output: bilingual_revision/rounds/{round_id}/user_annotations.json",
        f"generated_at: {now_iso()}",
        "ui_role: annotation_collector_only",
        "",
    ]
    if not check_only:
        write_text(path, "\n".join(lines))
        return [path.as_posix()]
    return []


def validate_annotations(
    annotations_doc: dict[str, Any],
    sentence_ids: set[str],
    paragraph_ids: set[str],
    section_ids: set[str],
    chapter_ids: set[str],
) -> list[str]:
    issues: list[str] = []
    annotations = annotations_doc.get("annotations", [])
    if not isinstance(annotations, list):
        return ["annotations is not a list"]
    for annotation in annotations:
        if not isinstance(annotation, dict):
            issues.append("annotation record is not an object")
            continue
        aid = first_value(annotation, "annotation_id", default="<unknown>")
        target = annotation.get("target", {})
        if not isinstance(target, dict):
            issues.append(f"{aid}: target is not an object")
            continue
        for key, known in (
            ("sentence_id", sentence_ids),
            ("after_sentence_id", sentence_ids),
            ("before_sentence_id", sentence_ids),
            ("paragraph_id", paragraph_ids),
            ("section_id", section_ids),
            ("chapter_id", chapter_ids),
        ):
            value = target.get(key)
            if value and str(value) not in known:
                issues.append(f"{aid}: unknown {key}={value}")
    return issues


def run_sync(args: argparse.Namespace) -> dict[str, Any]:
    workbench = args.workbench.resolve()
    bilingual = workbench / "bilingual_revision"
    round_dir = bilingual / "rounds" / args.round_id
    object_path = bilingual / "manuscript_objects.json"
    if not object_path.exists():
        raise FileNotFoundError(object_path)
    object_data = read_json(object_path)
    paper, objects = paper_and_objects(object_data)
    annotations_path = round_dir / "user_annotations.json"
    annotations_doc = load_annotations(annotations_path)
    decisions = annotations_doc.get("sentence_status_decisions", {})
    sentences = object_items(objects, "sentences")
    sentence_ids = {sentence_id(sentence) for sentence in sentences if sentence_id(sentence)}
    paragraph_ids = {first_value(item, "paragraph_id", "id") for item in object_items(objects, "paragraphs")}
    section_ids = {first_value(item, "section_id", "id") for item in object_items(objects, "sections")}
    chapter_ids = {first_value(item, "chapter_id", "id") for item in object_items(objects, "chapters")}

    written: list[str] = []
    warnings: list[str] = []
    issues = validate_annotations(annotations_doc, sentence_ids, paragraph_ids, section_ids, chapter_ids)

    if not args.check_only:
        ui_result = ui_resources.ensure_resources(workbench, overwrite=args.overwrite_shared, max_terms=args.max_terms)
        written.extend(ui_result.get("written", []))

    terminology_summary, terminology_written = sync_terminology(workbench, objects, args.check_only)
    written.extend(terminology_written)

    outputs = {
        bilingual / "manuscript_objects.md": render_manuscript_summary(paper, objects),
        bilingual / "latest_full_bilingual_review.md": render_full_review(paper, objects, decisions, args.round_id),
        bilingual / "partial_failed_sentence_review.md": render_partial_review(paper, objects, annotations_doc, args.round_id),
    }
    if not args.check_only:
        for path, text in outputs.items():
            write_text(path, text)
            written.append(path.as_posix())
    written.extend(update_manifest(workbench, paper, args.round_id, args.check_only))

    full_count = len(re.findall(r"^###\s+S", outputs[bilingual / "latest_full_bilingual_review.md"], flags=re.M))
    partial_ids = set(re.findall(r"\|\s*(S[\w.-]*\d[\w.-]*)\s*\|", outputs[bilingual / "partial_failed_sentence_review.md"]))
    unknown_partial = sorted(partial_ids - sentence_ids)
    if full_count != len(sentences):
        issues.append(f"full review sentence count mismatch: full={full_count} objects={len(sentences)}")
    if unknown_partial:
        issues.append("partial review contains unknown sentence ids: " + ", ".join(unknown_partial))
    if terminology_summary["missing_field"]:
        warnings.append(f"{terminology_summary['missing_field']} terminology records lack field/domain")
    if terminology_summary["missing_source_provenance"]:
        warnings.append(f"{terminology_summary['missing_source_provenance']} terminology records lack source provenance")

    report = {
        "generated_at": now_iso(),
        "workbench": workbench.as_posix(),
        "round": args.round_id,
        "mode": "check_only" if args.check_only else "write",
        "object_counts": {
            "chapters": len(object_items(objects, "chapters")),
            "sections": len(object_items(objects, "sections")),
            "paragraphs": len(object_items(objects, "paragraphs")),
            "sentences": len(sentences),
            "figure_table_text_objects": len(object_items(objects, "figure_table_text_objects")),
        },
        "annotation_counts": {
            "annotations": len(annotations_doc.get("annotations", []) if isinstance(annotations_doc.get("annotations"), list) else []),
            "sentence_status_decisions": len(decisions if isinstance(decisions, dict) else {}),
        },
        "written_files": written,
        "issues": issues,
        "warnings": warnings,
        "terminology_schema": terminology_summary,
        "review_drafts": {
            "full_sentence_count": full_count,
            "partial_sentence_count": len(partial_ids),
            "unknown_sentence_ids": unknown_partial,
        },
    }
    report_path = round_dir / "artifact_sync_report.json"
    if not args.check_only:
        write_json(report_path, report)
        report["written_files"].append(report_path.as_posix())
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize revision-control derived artifacts.")
    parser.add_argument("--workbench", required=True, type=Path, help="Path to revision_workbench")
    parser.add_argument("--round", default="round_001", dest="round_id", help="Round id")
    parser.add_argument("--check-only", action="store_true", help="validate and render in memory without writing files")
    parser.add_argument("--overwrite-shared", action="store_true", help="overwrite existing shared UI resources")
    parser.add_argument("--max-terms", type=int, default=80, help="max generated terms when shared resources are missing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = run_sync(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
