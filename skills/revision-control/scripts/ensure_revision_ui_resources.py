#!/usr/bin/env python3
"""Create project-level resources required by the revision annotation UI.

The script accepts either a revision_workbench path or a round path such as
revision_workbench/bilingual_revision/rounds/round_001. It creates shared
project standards, terminology, problem-word, and material-dependency files.
Terminology entries are generated as unconfirmed candidates from the current
manuscript object library so each paper project starts with its own glossary.
For bilingual projects, English terms also receive likely Chinese translations
from the aligned Chinese review text so both English and Chinese occurrences can
be highlighted in the annotation UI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


GENERIC_TERMS = {
    "English",
    "Chinese",
    "Abstract",
    "Introduction",
    "Conclusion",
    "Conclusions",
    "Table",
    "Figure",
    "Review",
    "Section",
    "References",
    "Data",
    "Author",
    "Manuscript",
    "Supplementary",
    "AI",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "computer science",
    "electronic information",
}


COMMON_WORDS = {
    "The",
    "This",
    "These",
    "Those",
    "Because",
    "However",
    "Moreover",
    "Therefore",
    "Although",
    "Existing",
    "Current",
    "Several",
    "Different",
    "Specific",
    "Important",
    "Compared",
    "Coupling",
    "During",
    "Based",
    "For",
    "With",
    "From",
    "Between",
    "Through",
    "Without",
    "When",
    "Where",
    "Why",
    "How",
}

BAD_EDGE_WORDS = {
    "and",
    "or",
    "of",
    "for",
    "with",
    "in",
    "on",
    "to",
    "from",
    "by",
    "as",
    "at",
    "the",
    "a",
    "an",
}


def now_note() -> str:
    return "generated_by: ensure_revision_ui_resources.py"


def resolve_workbench(path: Path) -> Path:
    current = path.resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / "bilingual_revision" / "manuscript_objects.json").exists():
            return candidate
        if candidate.name == "bilingual_revision" and (candidate / "manuscript_objects.json").exists():
            return candidate.parent
    raise FileNotFoundError(
        "Could not locate revision_workbench from path. Expected "
        "bilingual_revision/manuscript_objects.json above the provided path."
    )


def read_text_value(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value:
            return str(value)
    return ""


def load_sentence_pairs(object_path: Path) -> list[dict[str, str]]:
    data = json.loads(object_path.read_text(encoding="utf-8-sig"))
    paper = data.get("paper", data)
    objects = paper.get("objects", {}) if isinstance(paper, dict) else {}
    sentences = objects.get("sentences", []) if isinstance(objects, dict) else []
    pairs = []
    for sentence in sentences:
        if not isinstance(sentence, dict):
            continue
        english = read_text_value(sentence, "english_text")
        chinese = read_text_value(sentence, "chinese_review_text")
        if not english or not chinese:
            combined = read_text_value(sentence, "latest_text", "text", "original_text")
            english_match = re.search(r"English:\s*(.*?)(?:\n|\s*中文审阅稿:|$)", combined, flags=re.S)
            chinese_match = re.search(r"中文审阅稿:\s*(.*)$", combined, flags=re.S)
            english = english or (english_match.group(1).strip() if english_match else combined)
            chinese = chinese or (chinese_match.group(1).strip() if chinese_match else "")
        if english or chinese:
            pairs.append({"english": english, "chinese": chinese})
    return pairs


def clean_candidate(term: str) -> str:
    term = re.sub(r"\s+", " ", term).strip(" ,.;:()[]{}|\"'")
    term = re.sub(r"^(English|中文审阅稿|Chinese)\s*:\s*", "", term).strip()
    return term


def is_good_candidate(term: str) -> bool:
    if not term or len(term) < 3 or len(term) > 90:
        return False
    if term in GENERIC_TERMS or term.lower() in {item.lower() for item in GENERIC_TERMS}:
        return False
    if re.fullmatch(r"[\d\W_]+", term):
        return False
    if re.match(r"^[^A-Za-z0-9]", term):
        return False
    if re.search(r"[^A-Za-z0-9)]$", term):
        return False
    words = term.split()
    if words and words[0] in COMMON_WORDS:
        return False
    if words and (words[0].lower() in BAD_EDGE_WORDS or words[-1].lower() in BAD_EDGE_WORDS):
        return False
    if len(words) > 1 and len(words[0]) == 1 and words[0].islower():
        return False
    if len(words) == 1 and term.islower() and not re.search(r"[A-Z0-9-]", term):
        return False
    return True


def extract_abbreviations(text: str) -> list[str]:
    candidates = re.findall(r"\b[A-Z][A-Z0-9-]{1,}\b", text)
    return [item for item in candidates if is_good_candidate(item)]


def extract_capitalized_phrases(text: str) -> list[str]:
    pattern = re.compile(r"\b(?:[A-Z][a-zA-Z0-9-]+|[a-z]+-[a-zA-Z0-9-]+)(?:\s+(?:[A-Z][a-zA-Z0-9-]+|of|and|for|with|in|on|[a-z]+-[a-zA-Z0-9-]+)){1,5}")
    return [clean_candidate(match.group(0)) for match in pattern.finditer(text)]


def extract_domain_phrases(text: str) -> list[str]:
    suffixes = (
        "compounds",
        "compound",
        "catalysts",
        "catalyst",
        "plasma",
        "reactor",
        "reaction",
        "oxidation",
        "sulfide",
        "sulfur",
        "poisoning",
        "regeneration",
        "mineralization",
        "ozone",
        "radicals",
        "adsorption",
        "desorption",
        "surface",
        "species",
        "intermediates",
        "by-products",
    )
    suffix_re = "|".join(re.escape(item) for item in suffixes)
    pattern = re.compile(rf"\b[a-zA-Z0-9-]+(?:\s+[a-zA-Z0-9-]+){{0,4}}\s+(?:{suffix_re})\b", re.IGNORECASE)
    return [clean_candidate(match.group(0)) for match in pattern.finditer(text)]


def extract_chinese_terms(text: str) -> list[str]:
    suffixes = (
        "化合物",
        "硫化合物",
        "硫化氢",
        "硫醚",
        "二硫醚",
        "甲硫醇",
        "等离子体",
        "催化剂",
        "反应器",
        "反应",
        "氧化",
        "硫毒化",
        "毒化",
        "失活",
        "再生",
        "矿化",
        "臭氧",
        "自由基",
        "吸附",
        "脱附",
        "表面",
        "物种",
        "中间体",
        "副产物",
        "硫酸盐",
        "单质硫",
        "酸性气",
        "资源化",
    )
    results: list[str] = []
    for suffix in suffixes:
        pattern = re.compile(rf"[\u4e00-\u9fffA-Za-z0-9/-]{{0,14}}{re.escape(suffix)}")
        for match in pattern.finditer(text):
            term = match.group(0).strip("，。；：、（）()[] ")
            if 2 <= len(term) <= 24 and not term.startswith(("这些", "上述", "不同", "主要", "当前")):
                results.append(term)
    return results


KNOWN_TRANSLATIONS = {
    "VSC": ["挥发性硫化合物", "含硫污染物"],
    "VSCs": ["挥发性硫化合物", "含硫污染物"],
    "volatile sulfur compound": ["挥发性硫化合物"],
    "volatile sulfur compounds": ["挥发性硫化合物"],
    "hydrogen sulfide": ["硫化氢"],
    "H2S": ["硫化氢"],
    "methanethiol": ["甲硫醇"],
    "methyl mercaptan": ["甲硫醇"],
    "dimethyl sulfide": ["二甲基硫醚"],
    "DMS": ["二甲基硫醚"],
    "dimethyl disulfide": ["二甲基二硫醚"],
    "DMDS": ["二甲基二硫醚"],
    "CH3SH": ["甲硫醇"],
    "carbonyl sulfide": ["羰基硫"],
    "COS": ["羰基硫"],
    "carbon disulfide": ["二硫化碳"],
    "CS2": ["二硫化碳"],
    "sulfur dioxide": ["二氧化硫"],
    "SO2": ["二氧化硫"],
    "carbon dioxide": ["二氧化碳"],
    "CO2": ["二氧化碳"],
    "DBD": ["介质阻挡放电"],
    "nonthermal plasma": ["非热等离子体"],
    "non-thermal plasma": ["非热等离子体"],
    "NTP": ["非热等离子体"],
    "XPS": ["X射线光电子能谱", "XPS"],
    "DRIFTS": ["漫反射红外傅里叶变换光谱", "原位红外"],
    "DFT": ["密度泛函理论"],
    "BET": ["BET比表面积", "比表面积"],
    "LDH": ["层状双氢氧化物", "层状双氢氧化"],
    "PDS": ["过二硫酸盐"],
    "plasma-catalytic": ["等离子体催化", "等离子体-催化"],
    "direct plasma": ["直接等离子体"],
    "near-direct plasma": ["近直接等离子体"],
    "in-situ plasma": ["原位等离子体"],
    "in situ plasma": ["原位等离子体"],
    "residual ozone": ["残留臭氧"],
    "sulfur poisoning": ["硫毒化"],
    "elemental sulfur": ["单质硫"],
    "sulfate": ["硫酸盐"],
    "sulfates": ["硫酸盐"],
    "sulfur-containing intermediates": ["含硫中间体"],
    "sulfur-containing by-products": ["含硫副产物"],
    "dynamic regeneration": ["动态再生"],
    "excited species": ["激发态物种"],
    "acid gas": ["酸性气"],
    "acid-gas": ["酸性气"],
    "resource recovery": ["资源化", "资源回收"],
}

CHINESE_TOKEN_HINTS = {
    "acid": ["酸"],
    "adsorption": ["吸附"],
    "by-product": ["副产物", "产物"],
    "by-products": ["副产物", "产物"],
    "catalyst": ["催化"],
    "catalysts": ["催化"],
    "catalytic": ["催化"],
    "compound": ["化合物"],
    "compounds": ["化合物"],
    "deactivation": ["失活"],
    "desorption": ["脱附"],
    "excited": ["激发"],
    "gas": ["气"],
    "intermediate": ["中间体"],
    "intermediates": ["中间体"],
    "mineralization": ["矿化"],
    "oxidation": ["氧化"],
    "ozone": ["臭氧"],
    "plasma": ["等离子体"],
    "poisoning": ["毒化"],
    "radical": ["自由基"],
    "radicals": ["自由基"],
    "reaction": ["反应"],
    "reactor": ["反应器"],
    "regeneration": ["再生"],
    "resource": ["资源"],
    "species": ["物种"],
    "sulfate": ["硫酸盐"],
    "sulfates": ["硫酸盐"],
    "sulfide": ["硫"],
    "sulfur": ["硫"],
    "surface": ["表面"],
}

BAD_CHINESE_TRANSLATION_STARTS = (
    "上述",
    "这些",
    "不同",
    "主要",
    "当前",
    "因为",
    "而且",
    "需要",
    "通过",
    "部分",
    "研究",
    "提供",
    "测量",
)

GENERIC_CHINESE_TRANSLATIONS = {"反应", "表面", "吸附", "氧化", "再生", "催化剂", "等离子体"}
DEFAULT_FIELD = "environmental catalysis / plasma-catalytic treatment of volatile sulfur compounds"


def chinese_hint_groups(term: str) -> list[list[str]]:
    tokens = re.findall(r"[A-Za-z][A-Za-z-]*", term.lower())
    groups: list[list[str]] = []
    seen: set[str] = set()
    for token in tokens:
        hints = CHINESE_TOKEN_HINTS.get(token)
        if not hints:
            continue
        key = "\0".join(hints)
        if key in seen:
            continue
        seen.add(key)
        groups.append(hints)
    return groups


def is_likely_chinese_translation(term: str, chinese_term: str) -> bool:
    chinese_term = chinese_term.strip()
    if not chinese_term or chinese_term in GENERIC_CHINESE_TRANSLATIONS:
        return False
    if chinese_term.startswith(BAD_CHINESE_TRANSLATION_STARTS):
        return False
    hint_groups = chinese_hint_groups(term)
    if not hint_groups:
        return False
    if len(hint_groups) == 1:
        return any(hint in chinese_term for hint in hint_groups[0]) and len(chinese_term) >= 4
    matched = sum(1 for hints in hint_groups if any(hint in chinese_term for hint in hints))
    return matched >= min(2, len(hint_groups))


def likely_chinese_translations(term: str, sentence_pairs: list[dict[str, str]]) -> list[str]:
    known_first: list[str] = []
    candidates: Counter[str] = Counter()
    lower_term = term.lower()
    for known, translations in KNOWN_TRANSLATIONS.items():
        known_lower = known.lower()
        known_pattern = rf"(?<![A-Za-z0-9]){re.escape(known_lower)}(?![A-Za-z0-9])"
        if lower_term == known_lower or re.search(known_pattern, lower_term):
            for translation in translations:
                if translation not in known_first:
                    known_first.append(translation)
    if known_first:
        return known_first[:5]
    for pair in sentence_pairs:
        english = pair.get("english", "")
        chinese = pair.get("chinese", "")
        if not chinese or lower_term not in english.lower():
            continue
        for chinese_term in extract_chinese_terms(chinese):
            if is_likely_chinese_translation(term, chinese_term):
                candidates[chinese_term] += 1
    if candidates:
        return [item for item, _ in candidates.most_common(3)]
    return []


def generate_terminology(sentence_pairs: list[dict[str, str]], max_terms: int) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    variants: dict[str, set[str]] = {}
    for pair in sentence_pairs:
        text = pair.get("english", "")
        for extractor in (extract_abbreviations, extract_capitalized_phrases, extract_domain_phrases):
            for raw in extractor(text):
                term = clean_candidate(raw)
                if not is_good_candidate(term):
                    continue
                key = term.lower()
                counter[key] += 1
                variants.setdefault(key, set()).add(term)
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    terms: list[dict[str, Any]] = []
    for key, count in ranked:
        forms = sorted(variants.get(key, []), key=lambda value: (-len(value), value))
        term = forms[0] if forms else key
        if count < 2 and not re.fullmatch(r"[A-Z][A-Z0-9-]{1,}", term):
            continue
        accepted = [form for form in forms[1:] if form != term]
        chinese_translations = likely_chinese_translations(term, sentence_pairs)
        terms.append(
            {
                "term": term,
                "language": "en",
                "preferred_form": term,
                "accepted_variants": accepted,
                "chinese_translations": chinese_translations,
                "forbidden_variants": [],
                "field": DEFAULT_FIELD,
                "term_type": infer_term_type(term),
                "source_provenance": source_provenance_for_term(term, sentence_pairs),
                "reason": "Auto-generated bilingual candidate from manuscript object library; Chinese translations are inferred from the aligned Chinese review text and should be confirmed, edited, or deleted before treating as project standards.",
                "confirmed": False,
            }
        )
        if len(terms) >= max_terms:
            break
    return terms


def infer_term_type(term: str) -> str:
    if re.fullmatch(r"[A-Z][A-Z0-9-]{1,}", term):
        return "abbreviation"
    if re.search(r"\b(?:H2S|CO2|SO2|NOx|COS|CS2|CH3SH|CH3S)\b", term):
        return "chemical_species"
    if re.search(r"\b(?:XPS|DRIFTS|DFT|BET|DBD|LDH|PDS)\b", term):
        return "instrument_or_method"
    if re.search(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", term):
        return "proper_noun_or_named_method"
    return "professional_term"


def source_provenance_for_term(term: str, sentence_pairs: list[dict[str, str]]) -> list[str]:
    lower_term = term.lower()
    locations: list[str] = []
    for index, pair in enumerate(sentence_pairs, start=1):
        english = pair.get("english", "")
        if lower_term in english.lower():
            citations = "; ".join(re.findall(r"\[@([^\]]+)\]", english))
            location = f"sentence_pair_{index}"
            if citations:
                location += f"; citations: {citations}"
            locations.append(location)
        if len(locations) >= 5:
            break
    return locations or ["auto-generated from manuscript object library; source sentence not uniquely located"]


def quote(value: Any) -> str:
    return json.dumps(str(value or ""), ensure_ascii=False)


def write_if_missing(path: Path, text: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def terminology_yaml(terms: list[dict[str, Any]]) -> str:
    if not terms:
        return "terminology_glossary: []\n"
    lines = ["terminology_glossary:"]
    for item in terms:
        lines.append(f"  - term: {quote(item['term'])}")
        lines.append(f"    language: {quote(item.get('language', ''))}")
        lines.append(f"    preferred_form: {quote(item.get('preferred_form', item['term']))}")
        for key in ("accepted_variants", "chinese_translations", "forbidden_variants", "source_provenance"):
            values = item.get(key, []) or []
            if values:
                lines.append(f"    {key}:")
                for value in values:
                    lines.append(f"      - {quote(value)}")
            else:
                lines.append(f"    {key}: []")
        lines.append(f"    field: {quote(item.get('field', DEFAULT_FIELD))}")
        lines.append(f"    term_type: {quote(item.get('term_type', infer_term_type(str(item.get('term', '')))))}")
        lines.append(f"    reason: {quote(item.get('reason', ''))}")
        lines.append("    confirmed: false")
    return "\n".join(lines) + "\n"


def markdown_escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def terminology_md(terms: list[dict[str, Any]]) -> str:
    lines = [
        "# Terminology Glossary",
        "",
        "This glossary is project-specific. Auto-generated entries are candidates, not confirmed standards.",
        "Confirm, edit, or delete entries in the UI before relying on them during revision.",
        "Every entry should record its field/domain and source provenance so project-specific terms do not import unrelated disciplinary jargon.",
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
                    markdown_escape_cell(item.get("field", DEFAULT_FIELD)),
                    markdown_escape_cell(item.get("term_type", infer_term_type(str(item.get("term", ""))))),
                    markdown_escape_cell("; ".join(item.get("source_provenance", []) or [])),
                    markdown_escape_cell(", ".join(item.get("forbidden_variants", []) or [])),
                    "no",
                    markdown_escape_cell(item.get("reason", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def project_standards_yaml() -> str:
    return """project_review_standards:
  version: "1.0"
  project_profile:
    research_field: ""
    target_venue_or_standard: ""
    manuscript_type: ""
    terminology_scope_note: "Use field-specific terminology from this manuscript's discipline. Avoid importing artificial-intelligence, computer-science, or electronic-information jargon unless it is genuinely part of the paper's field or explicitly confirmed by the user. Generic terms broadly understood across fields do not need special restriction."
  confirmed_rules: []
  candidate_rules:
    - candidate_rule_id: "CAND_FIELD_TERMINOLOGY_001"
      source: "default revision-control UI resource template"
      proposed_rule: "During user-comment-based revision, preserve discipline-appropriate terminology and avoid unnecessary AI/computer/electronic-information proper nouns or jargon unless the project field requires them or the user confirms them."
      reason: "Prevents cross-field terminology contamination when generic skill-level review standards are applied to a specific paper project."
      status: "candidate_only"
      requires_user_confirmation: true
"""


def project_standards_md() -> str:
    return """# Project Supplemental Review Standards

This file records project-specific standards that supplement the general skill-level review standards.

## Project Profile

- Research field:
- Target venue or standard:
- Manuscript type:

## Default Candidate Standard

When revising from user annotations, preserve terminology appropriate to this paper's research field. Avoid unnecessary artificial-intelligence, computer-science, or electronic-information proper nouns and jargon unless they are genuinely part of the paper's field or explicitly confirmed by the user. Generic terms and concepts that are broadly understood across most academic fields do not require special restriction.

## Confirmed Rules

None yet.

## Candidate Rules

| candidate rule id | proposed rule | reason | status |
|---|---|---|---|
| CAND_FIELD_TERMINOLOGY_001 | Preserve discipline-appropriate terminology and avoid unnecessary AI/computer/electronic-information jargon unless required by the project field or confirmed by the user. | Prevents cross-field terminology contamination when general review standards are applied to a specific paper project. | candidate_only |
"""


def problem_words_yaml() -> str:
    return "problem_words: []\n"


def problem_words_md() -> str:
    return """# Problem Words

This file records project-specific banned, risky, or user-disliked expressions.

Current status: no project-specific problem words have been recorded yet.

| expression | scope | risk | replacement guidance | confirmed |
|---|---|---|---|---|
"""


def material_dependencies_yaml() -> str:
    return "materials: []\n"


def material_dependencies_md() -> str:
    return """# Material Dependencies

This file records supporting materials used by the revision workflow. Supporting materials are dependencies, not manuscript objects.

Current status: no supporting materials have been registered yet.

| material id | path | type | purpose | access state | verification state | related object ids | change state | notes |
|---|---|---|---|---|---|---|---|---|
"""


def ensure_resources(workbench: Path, overwrite: bool, max_terms: int) -> dict[str, Any]:
    shared = workbench / "shared"
    object_path = workbench / "bilingual_revision" / "manuscript_objects.json"
    sentence_pairs = load_sentence_pairs(object_path) if object_path.exists() else []
    terms = generate_terminology(sentence_pairs, max_terms=max_terms)
    files = {
        "project_review_standards.yaml": project_standards_yaml(),
        "project_review_standards.md": project_standards_md(),
        "terminology_glossary.yaml": terminology_yaml(terms),
        "terminology_glossary.md": terminology_md(terms),
        "problem_words.yaml": problem_words_yaml(),
        "problem_words.md": problem_words_md(),
        "material_dependencies.yaml": material_dependencies_yaml(),
        "material_dependencies.md": material_dependencies_md(),
    }
    written = []
    skipped = []
    for name, text in files.items():
        path = shared / name
        if write_if_missing(path, text, overwrite=overwrite):
            written.append(path.as_posix())
        else:
            skipped.append(path.as_posix())
    return {"workbench": workbench.as_posix(), "terms_generated": len(terms), "written": written, "skipped_existing": skipped}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ensure revision annotation UI project resources exist.")
    parser.add_argument("--path", required=True, type=Path, help="revision_workbench path or a path inside it, such as rounds/round_001")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing shared resource files")
    parser.add_argument("--max-terms", type=int, default=80, help="maximum auto-generated terminology candidates")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    workbench = resolve_workbench(args.path)
    result = ensure_resources(workbench, overwrite=args.overwrite, max_terms=args.max_terms)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
