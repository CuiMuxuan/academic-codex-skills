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
        self.object_path = self.bilingual_dir / "manuscript_objects.json"
        self.round_dir = self.bilingual_dir / "rounds" / round_id
        self.annotation_path = self.round_dir / "user_annotations.json"

    def source_object_library(self) -> str:
        try:
            return self.object_path.relative_to(self.workbench).as_posix()
        except ValueError:
            return self.object_path.as_posix()

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
            "title": first_value(paper, "title", "name", default="Untitled manuscript"),
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
        if not isinstance(data["annotations"], list):
            data["annotations"] = []
        return data

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
        tmp = self.annotation_path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        tmp.replace(self.annotation_path)
        return document

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


def object_list(objects: dict[str, Any], *names: str) -> list[dict[str, Any]]:
    for name in names:
        value = objects.get(name)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def normalize_tree(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    paper = data.get("paper", data)
    if not isinstance(paper, dict):
        paper = {}
    objects = paper.get("objects") or data.get("objects") or {}
    if not isinstance(objects, dict):
        objects = {}

    paper_id = first_value(paper, "paper_id", "id", default="P001")
    title = first_value(paper, "title", "name", default="Untitled manuscript")
    root = node("paper", paper_id, title=title, paper_id=paper_id)

    chapters = object_list(objects, "chapters", "chapter")
    sections = object_list(objects, "sections", "section")
    paragraphs = object_list(objects, "paragraphs", "paragraph")
    sentences = object_list(objects, "sentences", "sentence")
    figure_texts = object_list(objects, "figure_table_text_objects", "figure_table_text")

    chapter_nodes: dict[str, dict[str, Any]] = {}
    section_nodes: dict[str, dict[str, Any]] = {}
    paragraph_nodes: dict[str, dict[str, Any]] = {}
    sentence_nodes: dict[str, dict[str, Any]] = {}

    for index, chapter in enumerate(chapters, start=1):
        chapter_id = first_value(chapter, "chapter_id", "id", "node_id", default=f"CH_{index}")
        title = first_value(chapter, "title", "name", default=chapter_id)
        chapter_nodes[chapter_id] = node("chapter", chapter_id, title=title, chapter_id=chapter_id)

    for index, section in enumerate(sections, start=1):
        section_id = first_value(section, "section_id", "id", "node_id", default=f"SEC_{index}")
        title = first_value(section, "title", "heading", "name", default=section_id)
        chapter_id = first_value(section, "chapter_id", "parent_chapter_id", "parent_id", default="")
        section_nodes[section_id] = node(
            "section",
            section_id,
            title=title,
            section_id=section_id,
            chapter_id=chapter_id,
            local_purpose=section.get("local_purpose", ""),
            status=section.get("status", ""),
        )

    for index, paragraph in enumerate(paragraphs, start=1):
        paragraph_id = first_value(paragraph, "paragraph_id", "id", "node_id", default=f"P_{index}")
        title = first_value(paragraph, "title", "paragraph_role", default=paragraph_id)
        section_id = first_value(paragraph, "section_id", "parent_section_id", "parent_id", default="")
        paragraph_nodes[paragraph_id] = node(
            "paragraph",
            paragraph_id,
            title=title,
            paragraph_id=paragraph_id,
            section_id=section_id,
            paragraph_role=paragraph.get("paragraph_role", ""),
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
            status=first_value(sentence, "user_confirmed_status", "suggested_status", "status", default="pending"),
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
                    title="Unassigned sentences",
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
                        title="Unassigned paragraphs",
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

    if chapter_nodes:
        for chapter_node in chapter_nodes.values():
            root["children"].append(chapter_node)
        for section_id, section_node in section_nodes.items():
            if section_id not in used_section_ids:
                root["children"].append(section_node)
    else:
        for section_node in section_nodes.values():
            root["children"].append(section_node)

    for index, item in enumerate(figure_texts, start=1):
        object_id = first_value(item, "object_id", "id", "node_id", default=f"FT_{index}")
        text = first_value(item, "latest_text", "text", "original_text", default="")
        root["children"].append(
            node(
                "figure_table_text",
                object_id,
                title=first_value(item, "type", default=object_id),
                text=text,
                object_id=object_id,
                hash=stable_hash(text),
            )
        )

    paper_meta = {
        "paper_id": paper_id,
        "title": title,
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


HTML_PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revision Annotation UI</title>
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
    main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      min-height: calc(100vh - 52px);
    }
    #treePane {
      padding: 18px 22px 60px;
      overflow: auto;
    }
    #sidePane {
      border-left: 1px solid var(--border);
      background: var(--panel);
      padding: 16px;
      position: sticky;
      top: 52px;
      height: calc(100vh - 52px);
      overflow: auto;
    }
    .toolbar {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
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
      display: inline;
      line-height: 1.9;
      padding: 2px 3px;
      border-radius: 4px;
      cursor: text;
    }
    .sentence:hover {
      background: #eff6ff;
    }
    .gap-button {
      display: inline-flex;
      justify-content: center;
      align-items: center;
      width: 22px;
      height: 22px;
      margin: 0 4px;
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
    }
    .annotation-p0 { background: var(--p0); box-shadow: inset 3px 0 #dc2626; }
    .annotation-p1 { background: var(--p1); box-shadow: inset 3px 0 #f97316; }
    .annotation-p2 { background: var(--p2); box-shadow: inset 3px 0 #ca8a04; }
    .annotation-language { text-decoration: underline var(--language) 2px; }
    .annotation-structure { box-shadow: inset 3px 0 var(--structure); }
    .annotation-evidence { box-shadow: inset 3px 0 var(--evidence); }
    .annotation-selected { outline: 2px solid var(--accent); outline-offset: 2px; }
    label {
      display: block;
      font-size: 12px;
      font-weight: 700;
      color: #344054;
      margin: 12px 0 5px;
    }
    #sidePane select, #sidePane textarea, #sidePane input {
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
    .annotation-list-item {
      border-top: 1px solid #edf2f7;
      padding: 8px 0;
      cursor: pointer;
    }
    .annotation-list-item strong {
      color: var(--text);
      font-size: 12px;
    }
    .error {
      border: 1px solid #fecaca;
      background: #fef2f2;
      color: #991b1b;
      padding: 12px;
      border-radius: 8px;
    }
    @media (max-width: 900px) {
      main { grid-template-columns: 1fr; }
      #sidePane { position: static; height: auto; border-left: 0; border-top: 1px solid var(--border); }
    }
  </style>
</head>
<body>
  <header>
    <h1>Revision Annotation UI</h1>
    <div class="meta" id="headerMeta">Loading...</div>
    <button id="manualSave">Save</button>
  </header>
  <main>
    <section id="treePane">
      <div class="toolbar">
        <label for="viewMode" style="margin:0">View</label>
        <select id="viewMode">
          <option value="full_manuscript">Full manuscript</option>
          <option value="failed_or_targeted">Failed / targeted</option>
        </select>
        <span id="saveState" class="meta"></span>
      </div>
      <div id="treeRoot">Loading manuscript...</div>
    </section>
    <aside id="sidePane">
      <h2 style="font-size:16px;margin:0 0 10px">Annotation</h2>
      <div id="targetBox" class="target-box">Select text, a sentence, a paragraph, a section, or an insertion marker.</div>

      <label for="issueType">Problem type</label>
      <select id="issueType"></select>

      <label for="severity">Severity</label>
      <select id="severity">
        <option value="">Not set</option>
        <option value="P0">P0</option>
        <option value="P1">P1</option>
        <option value="P2">P2</option>
      </select>

      <label for="suggestedAction">Suggested action</label>
      <select id="suggestedAction"></select>

      <label for="comment">Comment (optional)</label>
      <textarea id="comment" placeholder="Optional user comment"></textarea>

      <div class="button-row">
        <button class="primary" id="saveAnnotation">Save annotation</button>
        <button class="danger" id="deleteAnnotation">Delete</button>
      </div>

      <label>Status</label>
      <div id="statusBox" class="status-box">No annotation selected.</div>

      <label>Saved annotations</label>
      <div id="annotationList" class="list-box"></div>
    </aside>
  </main>
  <script>
    const PROBLEM_TYPES = __PROBLEM_TYPES__;
    const SUGGESTED_ACTIONS = __SUGGESTED_ACTIONS__;
    const DEFAULT_ACTION_BY_ISSUE = __DEFAULT_ACTION_BY_ISSUE__;
    let manuscript = null;
    let annotationDoc = null;
    let currentAnnotation = null;
    let saveTimer = null;

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

    function issueDefaultAction(issueType) {
      return DEFAULT_ACTION_BY_ISSUE[issueType] || 'direct_revision_candidate';
    }

    function fillSelects() {
      const issue = document.getElementById('issueType');
      issue.innerHTML = PROBLEM_TYPES.map(v => `<option value="${v}">${v}</option>`).join('');
      const action = document.getElementById('suggestedAction');
      action.innerHTML = SUGGESTED_ACTIONS.map(v => `<option value="${v}">${v}</option>`).join('');
    }

    async function loadAll() {
      try {
        const view = document.getElementById('viewMode').value;
        manuscript = await fetchJSON('/api/manuscript?view=' + encodeURIComponent(view));
        annotationDoc = await fetchJSON('/api/annotations');
        document.getElementById('headerMeta').textContent =
          `${manuscript.paper.title || 'Untitled'} | ${manuscript.round} | ${manuscript.annotation_path}`;
        renderTree();
        renderAnnotationList();
        setSaveState('Loaded');
      } catch (error) {
        document.getElementById('treeRoot').innerHTML = `<div class="error">${htmlEscape(error.message)}</div>`;
        setSaveState('Load failed');
      }
    }

    function renderTree() {
      const root = manuscript.root || {children: manuscript.tree || []};
      document.getElementById('treeRoot').innerHTML = renderNode(root);
      applyAnnotationHighlights();
    }

    function renderNode(n) {
      if (!n) return '';
      const id = htmlEscape(n.id || '');
      const title = htmlEscape(n.title || n.id || n.node_type);
      if (n.node_type === 'paper') {
        return `<article data-paper-id="${id}"><h2>${title}</h2>${(n.children || []).map(renderNode).join('')}</article>`;
      }
      if (n.node_type === 'chapter' || n.node_type === 'section') {
        const attr = n.node_type === 'chapter' ? 'data-chapter-id' : 'data-section-id';
        const commentType = n.node_type === 'chapter' ? 'chapter_comment' : 'section_comment';
        return `<details open ${attr}="${id}" data-node-type="${n.node_type}">
          <summary><span class="node-row"><span>${title}</span><span class="node-id">${id}</span>
          <button class="node-comment" onclick="event.preventDefault(); event.stopPropagation(); makeNodeAnnotation('${commentType}', '${id}')">Comment</button></span></summary>
          ${(n.children || []).map(renderNode).join('')}
        </details>`;
      }
      if (n.node_type === 'paragraph') {
        const children = n.children || [];
        let body = '';
        for (let i = 0; i < children.length; i++) {
          body += renderNode(children[i]);
          if (children[i].node_type === 'sentence' && i < children.length - 1 && children[i + 1].node_type === 'sentence') {
            body += `<button class="gap-button" title="Insert comment here" onclick="makeInsertAnnotation('${htmlEscape(children[i].sentence_id)}', '${htmlEscape(children[i + 1].sentence_id)}')">+</button>`;
          }
        }
        return `<div class="paragraph" data-paragraph-id="${id}">
          <div class="paragraph-head"><span>${title} <span class="node-id">${id}</span></span>
          <button class="node-comment" onclick="makeNodeAnnotation('paragraph_comment', '${id}')">Comment paragraph</button></div>
          <div>${body}</div>
        </div>`;
      }
      if (n.node_type === 'sentence') {
        const sid = htmlEscape(n.sentence_id || n.id);
        return `<span class="sentence" data-sentence-id="${sid}" data-paragraph-id="${htmlEscape(n.paragraph_id || '')}" data-hash="${htmlEscape(n.hash || '')}" onclick="sentenceClicked(event, '${sid}')">${htmlEscape(n.text || '')}</span>`;
      }
      if (n.node_type === 'figure_table_text') {
        return `<div class="figure-text" data-figure-table-text-id="${id}">
          <div class="paragraph-head"><span>${title} <span class="node-id">${id}</span></span>
          <button class="node-comment" onclick="makeNodeAnnotation('figure_table_text_comment', '${id}')">Comment</button></div>
          ${htmlEscape(n.text || '')}
        </div>`;
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
        if (t.sentence_id) selector = `[data-sentence-id="${CSS.escape(t.sentence_id)}"]`;
        else if (t.paragraph_id) selector = `[data-paragraph-id="${CSS.escape(t.paragraph_id)}"]`;
        else if (t.section_id) selector = `[data-section-id="${CSS.escape(t.section_id)}"]`;
        else if (t.chapter_id) selector = `[data-chapter-id="${CSS.escape(t.chapter_id)}"]`;
        if (selector) {
          document.querySelectorAll(selector).forEach(el => el.classList.add(...classes));
        }
      }
    }

    function closestFromNode(node, selector) {
      if (!node) return null;
      const el = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
      return el ? el.closest(selector) : null;
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
        setSaveState('Selection must stay within one sentence');
        return;
      }
      const pre = document.createRange();
      pre.selectNodeContents(startSentence);
      pre.setEnd(range.startContainer, range.startOffset);
      const charStart = pre.toString().length;
      const charEnd = charStart + selectedText.length;
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
        selected_text: selectedText.trim(),
        text_hash: await sha256(selectedText)
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

    function targetSummary(annotation) {
      const target = annotation?.target || {};
      return Object.entries(target).filter(([, v]) => v !== '').map(([k, v]) => `${k}: ${v}`).join('\n') || 'No target';
    }

    function showAnnotation(annotation, autosave) {
      currentAnnotation = structuredClone(annotation);
      document.getElementById('issueType').value = currentAnnotation.issue_type || 'language_style';
      document.getElementById('severity').value = currentAnnotation.severity || '';
      document.getElementById('suggestedAction').value = currentAnnotation.suggested_action || issueDefaultAction(currentAnnotation.issue_type);
      document.getElementById('comment').value = currentAnnotation.comment || '';
      document.getElementById('targetBox').textContent = targetSummary(currentAnnotation);
      document.getElementById('statusBox').textContent = `${currentAnnotation.annotation_id || 'new'} | ${currentAnnotation.annotation_type} | ${currentAnnotation.status || 'user_commented'}`;
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

    function scheduleSaveCurrent() {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(() => saveCurrent(), 450);
    }

    async function saveCurrent() {
      if (!currentAnnotation) return;
      updateCurrentFromPanel();
      if (!currentAnnotation.issue_type) {
        setSaveState('Problem type is required');
        return;
      }
      try {
        const result = await fetchJSON('/api/annotations', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({annotation: currentAnnotation})
        });
        annotationDoc = result;
        const saved = result.annotations.find(a => a.annotation_id === (currentAnnotation.annotation_id || result.last_saved_annotation_id));
        if (saved) currentAnnotation = structuredClone(saved);
        showAnnotation(currentAnnotation, false);
        renderAnnotationList();
        applyAnnotationHighlights();
        setSaveState('Saved');
      } catch (error) {
        setSaveState('Save failed: ' + error.message);
      }
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
        document.getElementById('targetBox').textContent = 'Select text, a sentence, a paragraph, a section, or an insertion marker.';
        document.getElementById('statusBox').textContent = 'No annotation selected.';
        renderAnnotationList();
        applyAnnotationHighlights();
        setSaveState('Deleted');
      } catch (error) {
        setSaveState('Delete failed: ' + error.message);
      }
    }

    async function manualSave() {
      try {
        annotationDoc = await fetchJSON('/api/save', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(annotationDoc || {})
        });
        setSaveState('Saved');
      } catch (error) {
        setSaveState('Save failed: ' + error.message);
      }
    }

    function renderAnnotationList() {
      const list = document.getElementById('annotationList');
      const annotations = annotationDoc?.annotations || [];
      if (!annotations.length) {
        list.innerHTML = '<div>No annotations yet.</div>';
        return;
      }
      list.innerHTML = annotations.map(a => `
        <div class="annotation-list-item" onclick="selectAnnotation('${htmlEscape(a.annotation_id)}')">
          <strong>${htmlEscape(a.annotation_id)} ${htmlEscape(a.issue_type)}</strong><br>
          ${htmlEscape(a.annotation_type)}<br>
          ${htmlEscape(targetSummary(a)).replace(/\n/g, '<br>')}
        </div>`).join('');
    }

    function selectAnnotation(id) {
      const annotation = (annotationDoc.annotations || []).find(a => a.annotation_id === id);
      if (annotation) showAnnotation(annotation, false);
    }

    function setSaveState(text) {
      document.getElementById('saveState').textContent = text;
    }

    document.addEventListener('mouseup', () => setTimeout(captureSelection, 0));
    document.getElementById('viewMode').addEventListener('change', loadAll);
    document.getElementById('saveAnnotation').addEventListener('click', saveCurrent);
    document.getElementById('deleteAnnotation').addEventListener('click', deleteCurrent);
    document.getElementById('manualSave').addEventListener('click', manualSave);
    for (const id of ['issueType', 'severity', 'suggestedAction', 'comment']) {
      document.getElementById(id).addEventListener('input', () => {
        if (id === 'issueType') {
          const issue = document.getElementById('issueType').value;
          document.getElementById('suggestedAction').value = issueDefaultAction(issue);
        }
        scheduleSaveCurrent();
      });
    }

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
            if parsed.path == "/api/manuscript":
                self.handle_get_manuscript(parse_qs(parsed.query))
                return
            if parsed.path == "/api/annotations":
                payload = self.state.load_annotations()
                payload["annotation_path"] = self.state.annotation_path.as_posix()
                self.send_json(payload)
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
            self.send_json({"error": "not found"}, status=404)
        except FileNotFoundError as exc:
            self.send_json({"error": str(exc)}, status=409)
        except Exception as exc:  # noqa: BLE001
            self.send_json({"error": str(exc)}, status=500)

    def handle_get_manuscript(self, query: dict[str, list[str]]) -> None:
        data = self.state.read_object_library()
        root, paper = normalize_tree(data)
        view = (query.get("view") or ["full_manuscript"])[0]
        failed_ids = sorted(self.state.failed_sentence_ids())
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
