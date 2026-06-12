#!/usr/bin/env python3
"""Rebuild a revision-control object library from the active main manuscript.

The script keeps existing sentence ids and bilingual sentence text from the
current object library, but rebuilds paragraph objects from the canonical main
manuscript's natural paragraphs and structural blocks.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path
from typing import Any


ABBREVIATIONS = ["Fig", "Eq", "Ref", "Refs", "No", "Nos", "Dr", "Prof", "vs", "e.g", "i.e", "al", "ca", "cf"]


def now_stamp() -> str:
    return dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    tmp.replace(path)


def rel_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def make_id(prefix: str, title: str, fallback_index: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", title.upper()).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    if not cleaned:
        cleaned = str(fallback_index)
    return f"{prefix}_{cleaned[:48]}"


def split_markdown_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n")) if block.strip()]


def split_structural_block(block: str) -> list[tuple[str, str]]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) > 1 and all(line.startswith("- ") for line in lines):
        return [("list_item", line[2:].strip()) for line in lines]
    if len(lines) > 1 and all(line.startswith("|") and line.endswith("|") for line in lines):
        rows: list[tuple[str, str]] = []
        separator = re.compile(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$")
        for line in lines:
            if separator.match(line):
                continue
            rows.append(("table_row", line))
        return rows or [("natural_paragraph", block)]
    if block.startswith("![](") or block.startswith("!["):
        return [("figure_or_table_text_reference", block)]
    if block.startswith("**Fig") or block.startswith("**Table") or block.startswith("Table "):
        return [("figure_or_table_text_reference", block)]
    return [("natural_paragraph", block)]


def parse_main_manuscript(path: Path) -> tuple[str, list[dict[str, Any]]]:
    blocks = split_markdown_blocks(path.read_text(encoding="utf-8-sig", errors="replace"))
    paper_title = ""
    chapters: list[dict[str, Any]] = []
    current_chapter: dict[str, Any] | None = None
    current_section: dict[str, Any] | None = None

    for block in blocks:
        heading = re.match(r"^(#+)\s+(.+)$", block)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if level == 1:
                paper_title = title
                continue
            if level == 2:
                current_chapter = {"title": title, "sections": []}
                chapters.append(current_chapter)
                current_section = {"title": title, "level": level, "blocks": []}
                current_chapter["sections"].append(current_section)
                continue
            if level == 3:
                if current_chapter is None:
                    current_chapter = {"title": "Front matter", "sections": []}
                    chapters.append(current_chapter)
                current_section = {"title": title, "level": level, "blocks": []}
                current_chapter["sections"].append(current_section)
                continue
            if current_section is not None:
                current_section["blocks"].append({"type": "subheading", "text": title})
            continue

        if current_section is None:
            current_chapter = {"title": "Front matter", "sections": []}
            chapters.append(current_chapter)
            current_section = {"title": "Front matter", "level": 2, "blocks": []}
            current_chapter["sections"].append(current_section)
        for block_type, block_text in split_structural_block(block):
            current_section["blocks"].append({"type": block_type, "text": block_text})

    return paper_title, chapters


def sentence_estimate(block_type: str, text: str) -> int:
    if block_type == "subheading":
        return 0
    if block_type in {"list_item", "table_row"}:
        return 1
    value = text.strip()
    if not value:
        return 0
    for index, abbreviation in enumerate(ABBREVIATIONS):
        value = re.sub(r"\b" + re.escape(abbreviation) + r"\.", f"__ABBR{index}__", value)
    value = re.sub(r"(?<=\d)\.(?=\d)", "__DECIMAL__", value)
    parts = re.split(r"(?<=[.!?])\s+(?=(?:\[?[@A-Z0-9]))", value)
    return max(1, len([part for part in parts if part.strip()]))


def adjusted_counts(blocks: list[dict[str, Any]], sentence_total: int) -> list[int]:
    counts = [sentence_estimate(block["type"], block["text"]) for block in blocks]
    diff = sum(counts) - sentence_total
    if diff > 0:
        while diff > 0:
            candidates = [i for i, count in enumerate(counts) if count > 1]
            if not candidates:
                break
            index = max(candidates, key=lambda i: counts[i])
            counts[index] -= 1
            diff -= 1
    elif diff < 0:
        candidates = [i for i, count in enumerate(counts) if count > 0]
        if not candidates:
            candidates = list(range(len(counts)))
        while diff < 0 and candidates:
            index = max(candidates, key=lambda i: len(blocks[i]["text"]))
            counts[index] += 1
            diff += 1
    return counts


def paragraph_role(block_type: str) -> str:
    return {
        "natural_paragraph": "main-manuscript natural paragraph",
        "list_item": "main-manuscript list item",
        "table_row": "main-manuscript table row",
        "figure_or_table_text_reference": "main-manuscript figure/table text reference",
        "subheading": "main-manuscript subheading",
    }.get(block_type, block_type)


def backup_files(paths: list[Path], backup_dir: Path) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if path.exists():
            shutil.copy2(path, backup_dir / path.name)


def build_objects(
    current: dict[str, Any],
    paper_title: str,
    chapters: list[dict[str, Any]],
    workbench: Path,
    main_path: Path,
    alignment_path: Path,
    round_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    paper = current.get("paper", {})
    objects = paper.get("objects", {}) if isinstance(paper, dict) else {}
    old_chapters = [item for item in objects.get("chapters", []) if isinstance(item, dict)]
    old_sections = [item for item in objects.get("sections", []) if isinstance(item, dict)]
    old_sentences = [item for item in objects.get("sentences", []) if isinstance(item, dict)]

    old_section_counts: list[int] = []
    for section in old_sections:
        section_id = section.get("section_id") or section.get("id")
        old_section_counts.append(sum(1 for sentence in old_sentences if sentence.get("section_id") == section_id))

    flat_sections: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for chapter in chapters:
        for section in chapter["sections"]:
            flat_sections.append((chapter, section))
    if len(flat_sections) != len(old_sections):
        raise ValueError(f"section count mismatch: main={len(flat_sections)} existing={len(old_sections)}")

    new_chapters: list[dict[str, Any]] = []
    new_sections: list[dict[str, Any]] = []
    new_paragraphs: list[dict[str, Any]] = []
    new_sentences: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    sentence_to_context: dict[str, dict[str, str]] = {}

    old_sentence_cursor = 0
    paragraph_index = 0
    sentence_index = 0
    section_index = 0

    old_chapter_by_order = iter(old_chapters)
    previous_chapter_title: str | None = None
    current_chapter_obj: dict[str, Any] | None = None

    for chapter, section in flat_sections:
        if chapter["title"] != previous_chapter_title:
            old_chapter = next(old_chapter_by_order, {})
            chapter_id = old_chapter.get("chapter_id") or old_chapter.get("id") or make_id("CH", chapter["title"], len(new_chapters) + 1)
            current_chapter_obj = {
                "chapter_id": chapter_id,
                "title": chapter["title"],
                "section_ids": [],
            }
            new_chapters.append(current_chapter_obj)
            previous_chapter_title = chapter["title"]
        assert current_chapter_obj is not None

        old_section = old_sections[section_index]
        section_id = old_section.get("section_id") or old_section.get("id") or make_id("SEC", section["title"], section_index + 1)
        available_count = old_section_counts[section_index]
        assigned_counts = adjusted_counts(section["blocks"], available_count)
        diagnostics.append(
            {
                "section_id": section_id,
                "title": section["title"],
                "paragraph_blocks": len(section["blocks"]),
                "estimated_sentence_count": sum(sentence_estimate(block["type"], block["text"]) for block in section["blocks"]),
                "assigned_sentence_count": sum(assigned_counts),
                "existing_sentence_count": available_count,
            }
        )

        section_paragraph_ids: list[str] = []
        for block, count in zip(section["blocks"], assigned_counts):
            paragraph_index += 1
            paragraph_id = f"P_{paragraph_index:04d}"
            assigned_sentences = old_sentences[old_sentence_cursor : old_sentence_cursor + count]
            old_sentence_cursor += count
            sentence_ids = [sentence.get("sentence_id") or sentence.get("id") for sentence in assigned_sentences]
            sentence_ids = [str(sentence_id) for sentence_id in sentence_ids if sentence_id]
            section_paragraph_ids.append(paragraph_id)

            new_paragraphs.append(
                {
                    "paragraph_id": paragraph_id,
                    "section_id": section_id,
                    "title": f"Paragraph {paragraph_index}",
                    "paragraph_role": paragraph_role(block["type"]),
                    "source_paragraph_index": paragraph_index,
                    "source_block_type": block["type"],
                    "source_text": block["text"],
                    "sentence_ids": sentence_ids,
                    "status": "pending_user_annotation",
                }
            )

            for local_index, sentence in enumerate(assigned_sentences, start=1):
                sentence_index += 1
                copied = dict(sentence)
                sentence_id = str(copied.get("sentence_id") or copied.get("id") or f"S{sentence_index:04d}")
                copied["sentence_id"] = sentence_id
                copied["section_id"] = section_id
                copied["paragraph_id"] = paragraph_id
                copied["source_sentence_index"] = local_index
                copied["source_paragraph_index"] = paragraph_index
                copied["source_block_type"] = block["type"]
                copied["alignment_source_id"] = sentence_id
                copied["source_file"] = rel_path(alignment_path, workbench.parent)
                copied.setdefault("status", "pending_user_annotation")
                copied.setdefault("revision_count", 0)
                new_sentences.append(copied)
                sentence_to_context[sentence_id] = {
                    "chapter_id": str(current_chapter_obj["chapter_id"]),
                    "section_id": str(section_id),
                    "paragraph_id": str(paragraph_id),
                }

        new_section = dict(old_section)
        new_section.update(
            {
                "section_id": section_id,
                "chapter_id": current_chapter_obj["chapter_id"],
                "title": section["title"],
                "paragraph_ids": section_paragraph_ids,
                "source_heading_level": section.get("level", ""),
                "source_manuscript_path": rel_path(main_path, workbench.parent),
            }
        )
        new_sections.append(new_section)
        current_chapter_obj["section_ids"].append(section_id)
        section_index += 1

    if old_sentence_cursor != len(old_sentences):
        raise ValueError(f"sentence assignment mismatch: assigned={old_sentence_cursor} existing={len(old_sentences)}")

    new_paper = dict(paper)
    new_paper.update(
        {
            "title": paper_title or paper.get("title", ""),
            "language_mode": paper.get("language_mode", "english_chinese_sentence_aligned"),
            "source_manuscript_path": rel_path(main_path, workbench.parent),
            "alignment_review_source_path": rel_path(alignment_path, workbench.parent),
            "paragraph_source_mode": "main_manuscript",
            "current_round": round_id,
            "object_library_version": f"rebuilt_from_main_{now_iso()}",
            "objects": {
                "chapters": new_chapters,
                "sections": new_sections,
                "paragraphs": new_paragraphs,
                "sentences": new_sentences,
                "figure_table_text_objects": objects.get("figure_table_text_objects", []),
            },
        }
    )
    rebuilt = {
        "paper": new_paper,
        "id_mapping_history": current.get("id_mapping_history", []),
        "rebuild_diagnostics": {
            "generated_at": now_iso(),
            "source_manuscript_path": rel_path(main_path, workbench.parent),
            "alignment_review_source_path": rel_path(alignment_path, workbench.parent),
            "paragraphs_before": len(objects.get("paragraphs", [])),
            "paragraphs_after": len(new_paragraphs),
            "sentences": len(new_sentences),
            "sections": diagnostics,
        },
    }
    return rebuilt, sentence_to_context


def migrate_annotations(path: Path, sentence_to_context: dict[str, dict[str, str]]) -> None:
    if not path.exists():
        return
    data = read_json(path)
    changed = False
    for annotation in data.get("annotations", []):
        if not isinstance(annotation, dict):
            continue
        target = annotation.get("target", {})
        if not isinstance(target, dict):
            continue
        sentence_id = target.get("sentence_id")
        if sentence_id and str(sentence_id) in sentence_to_context:
            target.update(sentence_to_context[str(sentence_id)])
            changed = True
        for key in ("after_sentence_id", "before_sentence_id"):
            linked = target.get(key)
            if linked and str(linked) in sentence_to_context:
                context = sentence_to_context[str(linked)]
                target.setdefault("chapter_id", context["chapter_id"])
                target.setdefault("section_id", context["section_id"])
                changed = True
    if "sentence_status_decisions" not in data or not isinstance(data["sentence_status_decisions"], dict):
        data["sentence_status_decisions"] = {}
        changed = True
    if changed:
        write_json(path, data)


def write_summary(path: Path, rebuilt: dict[str, Any], backup_dir: Path) -> None:
    paper = rebuilt["paper"]
    objects = paper["objects"]
    summary = [
        "# Rebuilt Bilingual Revision Manuscript Object Library",
        "",
        f"Generated at: {rebuilt['rebuild_diagnostics']['generated_at']}",
        f"Source manuscript: `{paper.get('source_manuscript_path', '')}`",
        f"Alignment/review source: `{paper.get('alignment_review_source_path', '')}`",
        f"Paragraph source mode: `{paper.get('paragraph_source_mode', '')}`",
        f"Backup directory: `{backup_dir.as_posix()}`",
        "",
        f"- Chapters: {len(objects.get('chapters', []))}",
        f"- Sections: {len(objects.get('sections', []))}",
        f"- Paragraphs / structural blocks: {len(objects.get('paragraphs', []))}",
        f"- Sentence units: {len(objects.get('sentences', []))}",
        "",
        "Paragraph objects are rebuilt from the active main manuscript's natural paragraphs, list items, table rows, and figure/table text-reference blocks. Sentence ids and bilingual sentence text are preserved from the previous sentence-aligned object library.",
        "",
    ]
    path.write_text("\n".join(summary), encoding="utf-8", newline="\n")


def update_manifest(path: Path, workbench: Path, main_path: Path, alignment_path: Path, round_id: str) -> None:
    lines = [
        "paper_id: P_VSC_REVIEW_V0_31",
        "revision_mode: bilingual_main_manuscript_paragraphs",
        f"current_round: {round_id}",
        f"source_manuscript: {rel_path(main_path, workbench.parent)}",
        f"alignment_review_source: {rel_path(alignment_path, workbench.parent)}",
        "paragraph_source_mode: main_manuscript",
        "object_library: bilingual_revision/manuscript_objects.json",
        f"annotation_output: bilingual_revision/rounds/{round_id}/user_annotations.json",
        f"generated_at: {now_iso()}",
        "ui_role: annotation_collector_only",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild manuscript_objects.json from the active main manuscript.")
    parser.add_argument("--workbench", required=True, type=Path)
    parser.add_argument("--main", required=True, type=Path, help="Canonical active main manuscript markdown")
    parser.add_argument("--alignment", required=True, type=Path, help="Sentence-aligned bilingual review markdown")
    parser.add_argument("--round", default="round_001", dest="round_id")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workbench = args.workbench.resolve()
    bilingual_dir = workbench / "bilingual_revision"
    object_path = bilingual_dir / "manuscript_objects.json"
    summary_path = bilingual_dir / "manuscript_objects.md"
    manifest_path = bilingual_dir / "manifest.yaml"
    annotation_path = bilingual_dir / "rounds" / args.round_id / "user_annotations.json"
    for path in (object_path, args.main, args.alignment):
        if not path.exists():
            raise FileNotFoundError(path)

    current = read_json(object_path)
    paper_title, chapters = parse_main_manuscript(args.main)
    rebuilt, sentence_to_context = build_objects(
        current=current,
        paper_title=paper_title,
        chapters=chapters,
        workbench=workbench,
        main_path=args.main.resolve(),
        alignment_path=args.alignment.resolve(),
        round_id=args.round_id,
    )
    diagnostics = rebuilt["rebuild_diagnostics"]
    print(
        json.dumps(
            {
                "dry_run": args.dry_run,
                "chapters": len(rebuilt["paper"]["objects"]["chapters"]),
                "sections": len(rebuilt["paper"]["objects"]["sections"]),
                "paragraphs_before": diagnostics["paragraphs_before"],
                "paragraphs_after": diagnostics["paragraphs_after"],
                "sentences": diagnostics["sentences"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if args.dry_run:
        return 0

    backup_dir = bilingual_dir / "backups" / f"object_library_rebuild_{now_stamp()}"
    backup_files([object_path, summary_path, manifest_path, annotation_path], backup_dir)
    write_json(object_path, rebuilt)
    write_summary(summary_path, rebuilt, backup_dir)
    update_manifest(manifest_path, workbench, args.main.resolve(), args.alignment.resolve(), args.round_id)
    migrate_annotations(annotation_path, sentence_to_context)
    print(f"backup_dir={backup_dir}")
    print(f"wrote={object_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
