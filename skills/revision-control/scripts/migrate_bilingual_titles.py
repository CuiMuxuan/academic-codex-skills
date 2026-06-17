#!/usr/bin/env python3
"""Add or update bilingual title fields in a revision-control object library."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path
from typing import Any


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


def resolve_object_path(path: Path) -> Path:
    current = path.resolve()
    if current.is_file():
        return current
    if current.name == "bilingual_revision":
        return current / "manuscript_objects.json"
    return current / "bilingual_revision" / "manuscript_objects.json"


def object_lists(data: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    paper = data.get("paper", data)
    if not isinstance(paper, dict):
        raise ValueError("object library must contain a paper object")
    objects = paper.get("objects", {})
    if not isinstance(objects, dict):
        raise ValueError("paper.objects must be a JSON object")
    chapters = [item for item in objects.get("chapters", []) if isinstance(item, dict)]
    sections = [item for item in objects.get("sections", []) if isinstance(item, dict)]
    return paper, chapters, sections


def map_lookup(mapping: dict[str, Any], group: str, item_id: str, title: str) -> str:
    grouped = mapping.get(group, {})
    if isinstance(grouped, dict):
        value = grouped.get(item_id) or grouped.get(title)
        if value:
            return str(value).strip()
    titles = mapping.get("titles", {})
    if isinstance(titles, dict) and title in titles:
        return str(titles[title]).strip()
    return ""


def apply_title_fields(
    item: dict[str, Any],
    zh_title: str,
    status: str,
    source: str,
) -> bool:
    original = dict(item)
    title = str(item.get("title") or item.get("name") or "").strip()
    existing_zh = str(item.get("title_zh") or item.get("chinese_title") or item.get("title_cn") or "").strip()
    title_zh = zh_title or existing_zh
    item["title_en"] = str(item.get("title_en") or title).strip()
    if title_zh:
        item["title_zh"] = title_zh
        if item["title_en"] and item["title_zh"] != item["title_en"]:
            item["bilingual_title"] = f"{item['title_en']}\n{item['title_zh']}"
        else:
            item["bilingual_title"] = item["title_en"] or item["title_zh"]
        item["title_translation_status"] = status
        item["title_translation_source"] = source
    else:
        item.setdefault("title_zh", "")
        item["bilingual_title"] = item["title_en"]
        item["title_translation_status"] = "missing"
        item["title_translation_source"] = source if source else "no bilingual title source provided"
    return item != original


def migrate_titles(
    object_path: Path,
    mapping: dict[str, Any],
    status: str,
    source: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    data = read_json(object_path)
    paper, chapters, sections = object_lists(data)
    changed = {"paper": 0, "chapters": 0, "sections": 0, "missing": []}

    paper_title = str(paper.get("title") or paper.get("name") or "").strip()
    paper_zh = ""
    paper_map = mapping.get("paper", {})
    if isinstance(paper_map, dict):
        paper_zh = str(paper_map.get("title_zh") or paper_map.get("zh") or paper_map.get(paper_title) or "").strip()
    if not paper_zh:
        paper_zh = map_lookup(mapping, "papers", str(paper.get("paper_id") or paper.get("id") or ""), paper_title)
    if apply_title_fields(paper, paper_zh, status, source):
        changed["paper"] = 1
    if not paper.get("title_zh"):
        changed["missing"].append(str(paper.get("paper_id") or paper.get("id") or "paper"))

    for chapter in chapters:
        item_id = str(chapter.get("chapter_id") or chapter.get("id") or "").strip()
        title = str(chapter.get("title") or chapter.get("name") or "").strip()
        if apply_title_fields(chapter, map_lookup(mapping, "chapters", item_id, title), status, source):
            changed["chapters"] += 1
        if not chapter.get("title_zh"):
            changed["missing"].append(item_id or title)

    for section in sections:
        item_id = str(section.get("section_id") or section.get("id") or "").strip()
        title = str(section.get("title") or section.get("heading") or section.get("name") or "").strip()
        if apply_title_fields(section, map_lookup(mapping, "sections", item_id, title), status, source):
            changed["sections"] += 1
        if not section.get("title_zh"):
            changed["missing"].append(item_id or title)

    return data, changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate bilingual title fields into manuscript_objects.json.")
    parser.add_argument("--workbench", type=Path, help="revision_workbench or bilingual_revision path")
    parser.add_argument("--object-library", type=Path, help="direct path to manuscript_objects.json")
    parser.add_argument("--map", required=True, type=Path, help="JSON title map with paper/chapters/sections/titles entries")
    parser.add_argument("--status", default="inferred", choices=["confirmed", "inferred", "missing", "not_applicable"])
    parser.add_argument("--source", default="", help="source label stored in title_translation_source")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.workbench and not args.object_library:
        raise ValueError("provide --workbench or --object-library")
    object_path = args.object_library.resolve() if args.object_library else resolve_object_path(args.workbench)
    if not object_path.exists():
        raise FileNotFoundError(object_path)
    mapping = read_json(args.map)
    source = args.source or f"title map: {args.map.as_posix()}"
    data, summary = migrate_titles(object_path, mapping, args.status, source)
    report = {
        "dry_run": args.dry_run,
        "object_library": object_path.as_posix(),
        "generated_at": now_iso(),
        **summary,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.dry_run:
        return 0
    backup_path = object_path.with_name(f"{object_path.stem}.title_migration_backup_{now_stamp()}{object_path.suffix}")
    shutil.copy2(object_path, backup_path)
    write_json(object_path, data)
    print(f"backup={backup_path}")
    print(f"wrote={object_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
