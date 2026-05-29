#!/usr/bin/env python3
"""Validate academic Codex skills in this repository or an installed Codex home."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - reported as an actionable error.
    yaml = None


CORE_SKILLS = {
    "academic-paper-orchestrator",
    "paper-writing-workflow",
    "academic-research-verification",
    "post-manuscript-benchmark-review",
}

MANAGED_SKILLS = {
    "academic-de-ai-polishing",
    "academic-figure-workflow",
    "academic-formatting-workflow",
    "academic-paper-orchestrator",
    "academic-research-verification",
    "paper-writing-workflow",
    "pdf-docx-parsing-workflow",
    "post-manuscript-benchmark-review",
}

REQUIRED_SHARED_FILES = {
    "workflow-protocol-index.md",
    "trigger-conflict-matrix.md",
    "handoff-field-schema.md",
    "validation-policy.md",
}

REQUIRED_REPO_SCRIPTS = {
    "validate_skills.py",
    "audit_claim_anchors.py",
    "validate_markdown_docx_package.py",
    "figure_package_check.py",
}

CANONICAL_FIELD_TOKENS = {
    "current_mode",
    "material_id",
    "claim_anchor_id",
    "lit_gap_id",
    "allowed_claim_strength",
    "verification_state",
    "access_level",
    "gap_severity",
}


@dataclass
class Finding:
    level: str
    path: str
    message: str


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add(findings: list[Finding], level: str, path: Path | str, message: str, root: Path) -> None:
    findings.append(Finding(level, rel(path, root) if isinstance(path, Path) else path, message))


def detect_quick_validate() -> Path | None:
    candidates: list[Path] = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        candidates.append(Path(userprofile) / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    home = Path.home()
    candidates.append(home / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def parse_frontmatter(skill_md: Path, root: Path, findings: list[Finding]) -> dict[str, str] | None:
    text = skill_md.read_text(encoding="utf-8-sig", errors="replace")
    if not text.startswith("---"):
        add(findings, "error", skill_md, "missing YAML frontmatter", root)
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        add(findings, "error", skill_md, "unterminated YAML frontmatter", root)
        return None
    if yaml is None:
        add(findings, "error", skill_md, "PyYAML is not available", root)
        return None
    try:
        data = yaml.safe_load(parts[1])
    except Exception as exc:  # noqa: BLE001
        add(findings, "error", skill_md, f"invalid YAML frontmatter: {exc}", root)
        return None
    if not isinstance(data, dict):
        add(findings, "error", skill_md, "frontmatter must be an object", root)
        return None
    keys = set(data)
    if keys != {"name", "description"}:
        add(findings, "error", skill_md, f"frontmatter fields must be only name/description, got {sorted(keys)}", root)
    if not data.get("name"):
        add(findings, "error", skill_md, "missing frontmatter name", root)
    if not data.get("description"):
        add(findings, "error", skill_md, "missing frontmatter description", root)
    return {str(k): str(v) for k, v in data.items()}


def markdown_links(text: str) -> Iterable[str]:
    for target in re.findall(r"\[[^\]]+\]\(([^)\n]+)\)", text):
        if "://" in target or target.startswith("mailto:") or target.startswith("#"):
            continue
        clean = target.split("#", 1)[0].strip()
        if clean:
            yield clean


def managed_skill_dirs(root: Path) -> list[Path]:
    skills = root / "skills"
    if not skills.exists():
        return []
    return [skills / name for name in sorted(MANAGED_SKILLS) if (skills / name).is_dir()]


def managed_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for skill_dir in managed_skill_dirs(root):
        files.extend(skill_dir.glob("**/*.md"))
    shared = root / "shared"
    if shared.exists():
        files.extend(shared.glob("**/*.md"))
    return sorted(files)


def check_markdown_links(root: Path, findings: list[Finding]) -> None:
    for md in managed_markdown_files(root):
        text = md.read_text(encoding="utf-8-sig", errors="replace")
        for target in markdown_links(text):
            target_path = (md.parent / target).resolve()
            if not target_path.exists():
                add(findings, "error", md, f"broken Markdown link: {target}", root)


def check_skill_references(root: Path, skill_md: Path, findings: list[Finding]) -> None:
    text = skill_md.read_text(encoding="utf-8-sig", errors="replace")
    for target in markdown_links(text):
        if target.startswith("references/") or target.startswith("../../shared/"):
            target_path = (skill_md.parent / target).resolve()
            if not target_path.exists():
                add(findings, "error", skill_md, f"missing linked reference/shared file: {target}", root)


def check_yaml_and_json(root: Path, findings: list[Finding]) -> None:
    if yaml is None:
        add(findings, "error", root, "PyYAML is not available", root)
        return
    for skill_dir in managed_skill_dirs(root):
        path = skill_dir / "agents" / "openai.yaml"
        if not path.exists():
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            add(findings, "error", path, f"invalid YAML: {exc}", root)
    for skill_dir in managed_skill_dirs(root):
        path = skill_dir / "test-prompts.json"
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            add(findings, "error", path, f"invalid JSON: {exc}", root)


def check_python_scripts(root: Path, findings: list[Finding]) -> None:
    script_paths: list[Path] = []
    for skill_dir in managed_skill_dirs(root):
        script_paths.extend(skill_dir.glob("**/*.py"))
    script_paths.extend((root / "scripts").glob("*.py"))
    for path in sorted(script_paths):
        try:
            cache_path = Path(tempfile.gettempdir()) / "academic_codex_skill_validation" / (str(abs(hash(path.resolve()))) + ".pyc")
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            py_compile.compile(str(path), cfile=str(cache_path), doraise=True)
        except py_compile.PyCompileError as exc:
            add(findings, "error", path, f"Python syntax error: {exc.msg}", root)


def run_quick_validate(root: Path, findings: list[Finding]) -> None:
    quick_validate = detect_quick_validate()
    if quick_validate is None:
        add(findings, "warning", root, "quick_validate.py not found; skipped official skill validation", root)
        return
    for skill_dir in managed_skill_dirs(root):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(quick_validate), str(skill_dir)],
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0 or "Skill is valid!" not in output:
            add(findings, "error", skill_dir, f"quick_validate failed: {output}", root)


def check_shared(root: Path, findings: list[Finding]) -> None:
    shared = root / "shared"
    if not shared.exists():
        add(findings, "error", shared, "shared directory is missing", root)
        return
    present = {path.name for path in shared.glob("*.md")}
    for required in sorted(REQUIRED_SHARED_FILES - present):
        add(findings, "error", shared / required, "required shared protocol file is missing", root)

    schema = shared / "handoff-field-schema.md"
    if schema.exists():
        text = schema.read_text(encoding="utf-8-sig", errors="replace")
        for token in sorted(CANONICAL_FIELD_TOKENS):
            if token not in text:
                add(findings, "error", schema, f"canonical field token missing: {token}", root)


def check_repo_scripts(root: Path, findings: list[Finding]) -> None:
    scripts = root / "scripts"
    if not scripts.exists():
        repo_root = Path(__file__).resolve().parents[1]
        if root.resolve() == repo_root.resolve():
            add(findings, "error", scripts, "scripts directory is missing", root)
        return
    for name in sorted(REQUIRED_REPO_SCRIPTS):
        path = scripts / name
        if not path.exists():
            add(findings, "error", path, "required repository QA script is missing", root)
            continue
        result = subprocess.run([sys.executable, "-X", "utf8", str(path), "--help"], text=True, capture_output=True, check=False)
        if result.returncode != 0:
            add(findings, "error", path, f"--help smoke test failed: {(result.stdout + result.stderr).strip()}", root)


def check_core_alignment(root: Path, findings: list[Finding]) -> None:
    shared_ref = "../../../shared/handoff-field-schema.md"
    expected_refs = [
        root / "skills" / "paper-writing-workflow" / "references" / "claim-evidence-anchor-protocol.md",
        root / "skills" / "paper-writing-workflow" / "references" / "literature-gap-and-evidence-precheck.md",
        root / "skills" / "academic-research-verification" / "references" / "evidence-register-schema.md",
        root / "skills" / "academic-research-verification" / "references" / "literature-gap-verification-workflow.md",
        root / "skills" / "post-manuscript-benchmark-review" / "references" / "benchmark-report-schema.md",
    ]
    for path in expected_refs:
        if not path.exists():
            add(findings, "error", path, "expected core protocol reference is missing", root)
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if shared_ref not in text:
            add(findings, "warning", path, "does not explicitly point to shared handoff-field-schema.md", root)

    orchestrator = root / "skills" / "academic-paper-orchestrator" / "SKILL.md"
    if orchestrator.exists():
        text = orchestrator.read_text(encoding="utf-8-sig", errors="replace")
        for target in ("../../shared/workflow-protocol-index.md", "../../shared/trigger-conflict-matrix.md", "../../shared/handoff-field-schema.md"):
            if target not in text:
                add(findings, "error", orchestrator, f"orchestrator does not link shared protocol: {target}", root)


def check_skills(root: Path, findings: list[Finding]) -> None:
    skills = root / "skills"
    if not skills.exists():
        add(findings, "error", skills, "skills directory is missing", root)
        return
    for expected in sorted(MANAGED_SKILLS):
        if not (skills / expected).is_dir():
            add(findings, "error", skills / expected, "managed skill directory is missing", root)
    for skill_dir in managed_skill_dirs(root):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            add(findings, "error", skill_md, "SKILL.md is missing", root)
            continue
        data = parse_frontmatter(skill_md, root, findings)
        if data and data.get("name") != skill_dir.name:
            add(findings, "error", skill_md, f"frontmatter name does not match directory: {data.get('name')} != {skill_dir.name}", root)
        body_lines = len(skill_md.read_text(encoding="utf-8-sig", errors="replace").splitlines())
        if body_lines > 220:
            add(findings, "warning", skill_md, f"SKILL.md is long ({body_lines} lines); consider moving details to references", root)
        check_skill_references(root, skill_md, findings)


def validate(root: Path, strict: bool) -> int:
    findings: list[Finding] = []
    root = root.resolve()
    check_shared(root, findings)
    check_repo_scripts(root, findings)
    check_skills(root, findings)
    check_markdown_links(root, findings)
    check_yaml_and_json(root, findings)
    check_python_scripts(root, findings)
    run_quick_validate(root, findings)
    check_core_alignment(root, findings)

    errors = [item for item in findings if item.level == "error"]
    warnings = [item for item in findings if item.level == "warning"]

    print(f"root={root}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for item in findings:
        print(f"[{item.level}] {item.path}: {item.message}")

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root or Codex home containing skills/ and shared/")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()
    return validate(args.root, args.strict)


if __name__ == "__main__":
    sys.exit(main())
